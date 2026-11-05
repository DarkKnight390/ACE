import json
import unittest
from io import BytesIO
from types import ModuleType
from unittest.mock import patch

import httpx

from ace_voice.models import Message
from ace_voice.providers.elevenlabs import ElevenLabsTextToSpeech
from ace_voice.providers.faster_whisper import FasterWhisperSpeechRecognizer
from ace_voice.providers.nvidia import NvidiaLanguageModel


class ProviderAdapterTests(unittest.IsolatedAsyncioTestCase):
    async def test_nvidia_adapter_yields_streamed_text(self) -> None:
        body = (
            'data: {"choices":[{"delta":{"content":"Hello"}}]}\n\n'
            "data: [DONE]\n\n"
        )
        requests: list[httpx.Request] = []

        async def handler(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            return httpx.Response(200, content=body)

        async with httpx.AsyncClient(
            transport=httpx.MockTransport(handler)
        ) as client:
            model = NvidiaLanguageModel(
                client,
                base_url="https://nvidia.example/v1/",
                api_key="test-key",
                model="test-model",
            )
            chunks = [
                chunk
                async for chunk in model.stream(
                    [Message(role="user", content="Hi")]
                )
            ]

        self.assertEqual(chunks, ["Hello"])
        self.assertEqual(
            str(requests[0].url), "https://nvidia.example/v1/chat/completions"
        )
        self.assertTrue(requests[0].headers["Authorization"].startswith("Bearer "))
        self.assertTrue(json.loads(requests[0].content)["stream"])

    async def test_faster_whisper_transcribes_wav_and_reuses_model(self) -> None:
        model_options: list[tuple[str, dict[str, str]]] = []
        transcriptions: list[tuple[bytes, str | None]] = []

        class FakeSegment:
            def __init__(self, text: str) -> None:
                self.text = text

        class FakeWhisperModel:
            def __init__(self, model_size: str, **kwargs: str) -> None:
                model_options.append((model_size, kwargs))

            def transcribe(
                self, audio: BytesIO, *, language: str | None
            ) -> tuple[list[FakeSegment], None]:
                transcriptions.append((audio.read(), language))
                return [FakeSegment(" Book"), FakeSegment(" a table ")], None

        fake_module = ModuleType("faster_whisper")
        setattr(fake_module, "WhisperModel", FakeWhisperModel)
        recognizer = FasterWhisperSpeechRecognizer(
            model_size="base",
            device="cpu",
            compute_type="int8",
            language="en",
        )

        with patch.dict("sys.modules", {"faster_whisper": fake_module}):
            first = await recognizer.transcribe(b"wav-data")
            second = await recognizer.transcribe(b"more-wav")

        self.assertEqual(first, "Book a table")
        self.assertEqual(second, "Book a table")
        self.assertEqual(
            model_options,
            [("base", {"device": "cpu", "compute_type": "int8"})],
        )
        self.assertEqual(
            transcriptions, [(b"wav-data", "en"), (b"more-wav", "en")]
        )

    async def test_faster_whisper_rejects_empty_audio(self) -> None:
        recognizer = FasterWhisperSpeechRecognizer()
        with self.assertRaisesRegex(ValueError, "cannot be empty"):
            await recognizer.transcribe(b"")

    async def test_elevenlabs_adapter_yields_streamed_pcm(self) -> None:
        captured: list[httpx.Request] = []

        async def handler(request: httpx.Request) -> httpx.Response:
            captured.append(request)
            return httpx.Response(200, content=b"\x01\x00\x02\x00")

        async with httpx.AsyncClient(
            transport=httpx.MockTransport(handler)
        ) as client:
            tts = ElevenLabsTextToSpeech(
                client,
                api_key="tts-key",
                voice_id="voice-1",
                model="tts-test",
            )
            chunks = [chunk async for chunk in tts.stream("Hello.")]

        self.assertEqual(b"".join(chunks), b"\x01\x00\x02\x00")
        self.assertEqual(
            str(captured[0].url),
            "https://api.elevenlabs.io/v1/text-to-speech/voice-1/stream?output_format=pcm_24000",
        )
        self.assertEqual(captured[0].headers["xi-api-key"], "tts-key")
        self.assertEqual(json.loads(captured[0].content)["model_id"], "tts-test")


if __name__ == "__main__":
    unittest.main()
