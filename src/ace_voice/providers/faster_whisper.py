from __future__ import annotations

import asyncio
from io import BytesIO
from threading import Lock
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from faster_whisper import WhisperModel


class FasterWhisperSpeechRecognizer:
    def __init__(
        self,
        *,
        model_size: str = "small",
        device: str = "cpu",
        compute_type: str = "int8",
        language: str | None = None,
    ) -> None:
        self._model_size = model_size
        self._device = device
        self._compute_type = compute_type
        self._language = language
        self._model: WhisperModel | None = None
        self._model_lock = Lock()

    async def transcribe(self, wav_audio: bytes) -> str:
        if not wav_audio:
            raise ValueError("Audio input cannot be empty")
        return await asyncio.to_thread(self._transcribe_sync, wav_audio)

    def _transcribe_sync(self, wav_audio: bytes) -> str:
        with self._model_lock:
            if self._model is None:
                try:
                    from faster_whisper import WhisperModel
                except ImportError as exc:
                    raise RuntimeError(
                        "Faster-Whisper transcription requires the audio extra; "
                        'install it with "python -m pip install -e .[audio]"'
                    ) from exc
                self._model = WhisperModel(
                    self._model_size,
                    device=self._device,
                    compute_type=self._compute_type,
                )

            segments = self._model.transcribe(
                BytesIO(wav_audio),
                language=self._language,
            )[0]
            return " ".join(segment.text.strip() for segment in segments).strip()
