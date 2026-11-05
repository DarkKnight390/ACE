from __future__ import annotations

import httpx


class OpenAICompatibleSpeechRecognizer:
    """Adapter for transcription services exposing /audio/transcriptions."""

    def __init__(
        self,
        client: httpx.AsyncClient,
        *,
        base_url: str,
        model: str,
        api_key: str | None = None,
    ) -> None:
        self._client = client
        self._url = f"{base_url.rstrip('/')}/audio/transcriptions"
        self._model = model
        self._api_key = api_key

    async def transcribe(self, wav_audio: bytes) -> str:
        headers = (
            {"Authorization": f"Bearer {self._api_key}"}
            if self._api_key
            else {}
        )
        response = await self._client.post(
            self._url,
            headers=headers,
            data={"model": self._model},
            files={"file": ("utterance.wav", wav_audio, "audio/wav")},
        )
        response.raise_for_status()
        payload = response.json()
        transcript = payload.get("text") if isinstance(payload, dict) else None
        if not isinstance(transcript, str):
            raise ValueError("Transcription response must contain a string 'text' field")
        return transcript
