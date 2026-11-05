from __future__ import annotations

import asyncio
import io
import logging
import wave
from collections.abc import Callable

from ace_voice.ports import AudioSink


logger = logging.getLogger(__name__)


def _sounddevice():
    try:
        import sounddevice
    except ImportError as exc:
        raise RuntimeError(
            "Local microphone and playback require the audio extra; "
            'install it with "python -m pip install -e .[audio]"'
        ) from exc
    return sounddevice


class LocalAudioIO:
    def __init__(self, sample_rate: int, playback_sample_rate: int = 24000) -> None:
        self._sample_rate = sample_rate
        self._playback_sample_rate = playback_sample_rate

    def capture_until_enter(self) -> bytes:
        sounddevice = _sounddevice()
        blocks: list[bytes] = []

        def capture(
            indata: object, frames: int, time_info: object, status: object
        ) -> None:
            if status:
                logger.warning("Audio input status: %s", status)
            blocks.append(bytes(indata))

        print("Listening. Press Enter to stop recording.", flush=True)
        with sounddevice.InputStream(
            samplerate=self._sample_rate,
            channels=1,
            dtype="int16",
            callback=capture,
        ):
            input()
        raw_audio = b"".join(blocks)
        if not raw_audio:
            raise RuntimeError("No audio was captured from the microphone")
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self._sample_rate)
            wav_file.writeframes(raw_audio)
        return wav_buffer.getvalue()

    def open_playback(self) -> LocalAudioPlayback:
        return LocalAudioPlayback(self._playback_sample_rate)


class LocalAudioPlayback(AudioSink):
    def __init__(self, sample_rate: int) -> None:
        sounddevice = _sounddevice()
        self._stream = sounddevice.RawOutputStream(
            samplerate=sample_rate, channels=1, dtype="int16"
        )
        self._stream.start()
        self._pending = b""
        self._closed = False

    async def write(self, pcm_audio: bytes) -> None:
        if self._closed:
            raise RuntimeError("Audio playback is already closed")
        data = self._pending + pcm_audio
        aligned_length = len(data) - (len(data) % 2)
        self._pending = data[aligned_length:]
        if aligned_length:
            await asyncio.to_thread(self._stream.write, data[:aligned_length])

    async def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        try:
            if self._pending:
                raise ValueError("Received an incomplete PCM sample")
        finally:
            await asyncio.to_thread(self._stream.stop)
            await asyncio.to_thread(self._stream.close)
