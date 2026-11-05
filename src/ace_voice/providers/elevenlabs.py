from __future__ import annotations

from collections.abc import AsyncIterator

import httpx


class ElevenLabsTextToSpeech:
    def __init__(
        self,
        client: httpx.AsyncClient,
        *,
        api_key: str,
        voice_id: str,
        model: str,
    ) -> None:
        self._client = client
        self._url = (
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"
        )
        self._api_key = api_key
        self._model = model

    async def stream(self, text: str) -> AsyncIterator[bytes]:
        if not text.strip():
            raise ValueError("Text-to-speech input cannot be empty")
        headers = {
            "xi-api-key": self._api_key,
            "Accept": "audio/pcm",
        }
        params = {"output_format": "pcm_24000"}
        body = {"text": text, "model_id": self._model}
        async with self._client.stream(
            "POST", self._url, headers=headers, params=params, json=body
        ) as response:
            response.raise_for_status()
            async for chunk in response.aiter_bytes(chunk_size=4096):
                if chunk:
                    yield chunk
