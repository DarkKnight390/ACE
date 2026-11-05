import json
import unittest

import httpx

from ace_voice.models import Message
from ace_voice.providers.elevenlabs import ElevenLabsTextToSpeech
from ace_voice.providers.nvidia import NvidiaLanguageModel
from ace_voice.providers.openai_compatible_stt import (
    OpenAICompatibleSpeechRecognizer,
)


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
        self.assertEqual(requests[0].headers["Authorization"], "Bearer test-key")
        self.assertTrue(json.loads(requests[0].content)["stream"])

    async def test_transcription_adapter_posts_wav_and_returns_text(self) -> None:
        captured: list[httpx.Request] = []

        async def handler(request: httpx.Request) -> httpx.Response:
            captured.append(request)
            return httpx.Response(200, json={"text": "Book a table"})

        async with httpx.AsyncClient(
            transport=httpx.MockTransport(handler)
        ) as client:
            recognizer = OpenAICompatibleSpeechRecognizer(
                client,
                base_url="http://stt.example/v1",
                model="whisper-test",
                api_key="stt-key",
            )
            result = await recognizer.transcribe(b"wav-data")

        self.assertEqual(result, "Book a table")
        self.assertEqual(
            str(captured[0].url),
            "http://stt.example/v1/audio/transcriptions",
        )
        self.assertEqual(captured[0].headers["Authorization"], "Bearer stt-key")
        self.assertIn(b"filename=\"utterance.wav\"", captured[0].content)

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
