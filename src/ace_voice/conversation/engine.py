from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

from ace_voice.models import ConversationSession
from ace_voice.phrase_segmenter import PhraseSegmenter
from ace_voice.ports import AudioSink, LanguageModel, TextToSpeech


class SessionLogger(Protocol):
    async def record(
        self,
        session_id: str,
        event: str,
        metadata: dict[str, str | int | float | bool | None],
    ) -> None: ...


class VoiceConversationEngine:
    def __init__(
        self,
        language_model: LanguageModel,
        text_to_speech: TextToSpeech,
        session_logger: SessionLogger,
        *,
        max_phrase_chars: int = 180,
    ) -> None:
        self._language_model = language_model
        self._text_to_speech = text_to_speech
        self._session_logger = session_logger
        self._max_phrase_chars = max_phrase_chars

    async def respond(
        self,
        session: ConversationSession,
        user_text: str,
        *,
        on_text: Callable[[str], None],
        audio_sink: AudioSink,
    ) -> str:
        session.add_user_message(user_text)
        await self._session_logger.record(
            session.session_id,
            "user_turn",
            {"characters": len(user_text)},
        )
        segmenter = PhraseSegmenter(max_chars=self._max_phrase_chars)
        response_parts: list[str] = []
        phrase_count = 0

        async for delta in self._language_model.stream(session.model_messages()):
            response_parts.append(delta)
            on_text(delta)
            for phrase in segmenter.feed(delta):
                await self._speak(phrase, audio_sink)
                phrase_count += 1

        for phrase in segmenter.flush():
            await self._speak(phrase, audio_sink)
            phrase_count += 1

        response = "".join(response_parts)
        session.add_assistant_message(response)
        await self._session_logger.record(
            session.session_id,
            "assistant_turn",
            {"characters": len(response), "spoken_phrases": phrase_count},
        )
        return response

    async def _speak(self, phrase: str, audio_sink: AudioSink) -> None:
        async for audio_chunk in self._text_to_speech.stream(phrase):
            await audio_sink.write(audio_chunk)
