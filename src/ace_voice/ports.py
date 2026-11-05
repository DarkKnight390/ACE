from __future__ import annotations

from collections.abc import AsyncIterator, Mapping, Sequence
from typing import Protocol

from ace_voice.models import Message


class SpeechRecognizer(Protocol):
    async def transcribe(self, wav_audio: bytes) -> str: ...


class LanguageModel(Protocol):
    def stream(self, messages: Sequence[Message]) -> AsyncIterator[str]: ...


class TextToSpeech(Protocol):
    def stream(self, text: str) -> AsyncIterator[bytes]: ...


class AudioInput(Protocol):
    def capture_until_enter(self) -> bytes: ...


class AudioSink(Protocol):
    async def write(self, pcm_audio: bytes) -> None: ...


class BusinessToolExecutor(Protocol):
    async def execute(
        self,
        *,
        business_id: str,
        agent_id: str,
        tool_name: str,
        arguments: Mapping[str, object],
        idempotency_key: str,
    ) -> Mapping[str, object]: ...


class TelephonyTransport(Protocol):
    async def receive_audio(self) -> AsyncIterator[bytes]: ...

    async def send_audio(self, pcm_audio: bytes) -> None: ...

    async def end_call(self) -> None: ...
