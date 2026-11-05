import tempfile
import unittest
from pathlib import Path
from typing import AsyncIterator, Sequence

from ace_voice.conversation.engine import VoiceConversationEngine
from ace_voice.models import ConversationSession, Message
from ace_voice.session_log import JsonlSessionLogger


class FakeLanguageModel:
    def __init__(self, response: str) -> None:
        self.response = response
        self.requests: list[Sequence[Message]] = []

    async def stream(self, messages: Sequence[Message]) -> AsyncIterator[str]:
        self.requests.append(messages)
        for token in self.response.split(" "):
            yield token + " "


class FakeTextToSpeech:
    def __init__(self) -> None:
        self.phrases: list[str] = []

    async def stream(self, text: str) -> AsyncIterator[bytes]:
        self.phrases.append(text)
        yield text.encode("utf-8")


class FakeAudioSink:
    def __init__(self) -> None:
        self.chunks: list[bytes] = []

    async def write(self, pcm_audio: bytes) -> None:
        self.chunks.append(pcm_audio)


class VoiceConversationEngineTests(unittest.IsolatedAsyncioTestCase):
    async def test_streams_text_speaks_phrases_and_keeps_context(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            llm = FakeLanguageModel("Hello there. How can I help?")
            tts = FakeTextToSpeech()
            sink = FakeAudioSink()
            engine = VoiceConversationEngine(
                llm, tts, JsonlSessionLogger(Path(temp_dir) / "sessions.jsonl")
            )
            session = ConversationSession(
                messages=[Message(role="system", content="system prompt")]
            )
            visible_text: list[str] = []

            result = await engine.respond(
                session,
                "Hi",
                on_text=visible_text.append,
                audio_sink=sink,
            )

            self.assertEqual(result, "Hello there. How can I help? ")
            self.assertEqual("".join(visible_text), result)
            self.assertEqual(tts.phrases, ["Hello there.", "How can I help?"])
            self.assertEqual(
                sink.chunks, [b"Hello there.", b"How can I help?"]
            )
            self.assertEqual(
                [message.role for message in session.messages],
                ["system", "user", "assistant"],
            )

            await engine.respond(
                session,
                "Follow up",
                on_text=lambda _: None,
                audio_sink=FakeAudioSink(),
            )
            self.assertEqual(len(llm.requests[1]), 4)
            self.assertEqual(llm.requests[1][0].role, "system")
            self.assertEqual(llm.requests[1][1].content, "Hi")
            log_lines = (Path(temp_dir) / "sessions.jsonl").read_text(
                encoding="utf-8"
            ).splitlines()
            self.assertEqual(len(log_lines), 4)
            self.assertNotIn("Hi", "\n".join(log_lines))


if __name__ == "__main__":
    unittest.main()
