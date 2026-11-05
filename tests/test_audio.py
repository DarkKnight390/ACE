import io
import sys
import unittest
import wave
from types import SimpleNamespace
from unittest.mock import patch

from ace_voice.audio import LocalAudioIO


class FakeInputStream:
    def __init__(self, *, callback, **kwargs) -> None:
        self._callback = callback

    def __enter__(self):
        self._callback(b"\x01\x00\x02\x00", 2, None, None)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        return None


class FakeOutputStream:
    instances = []

    def __init__(self, **kwargs) -> None:
        self.writes = []
        self.started = False
        self.stopped = False
        self.closed = False
        self.__class__.instances.append(self)

    def start(self) -> None:
        self.started = True

    def write(self, data: bytes) -> None:
        self.writes.append(data)

    def stop(self) -> None:
        self.stopped = True

    def close(self) -> None:
        self.closed = True


class LocalAudioIOTests(unittest.IsolatedAsyncioTestCase):
    async def test_captures_wav_and_aligns_streamed_pcm(self) -> None:
        FakeOutputStream.instances.clear()
        sounddevice = SimpleNamespace(
            InputStream=FakeInputStream,
            RawOutputStream=FakeOutputStream,
        )
        audio_io = LocalAudioIO(sample_rate=16000)
        with patch.dict(sys.modules, {"sounddevice": sounddevice}):
            with patch("builtins.input", return_value=""):
                wav_audio = audio_io.capture_until_enter()
            with wave.open(io.BytesIO(wav_audio), "rb") as wav_file:
                self.assertEqual(wav_file.getframerate(), 16000)
                self.assertEqual(wav_file.getnchannels(), 1)
                self.assertEqual(wav_file.readframes(2), b"\x01\x00\x02\x00")

            playback = audio_io.open_playback()
            await playback.write(b"\x01")
            await playback.write(b"\x00\x02\x00")
            await playback.close()

        stream = FakeOutputStream.instances[0]
        self.assertTrue(stream.started)
        self.assertEqual(stream.writes, [b"\x01\x00\x02\x00"])
        self.assertTrue(stream.stopped)
        self.assertTrue(stream.closed)


if __name__ == "__main__":
    unittest.main()
