from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse


def _required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Required environment variable {name} is not set")
    return value


def _base_url(name: str, value: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"{name} must be an absolute HTTP(S) URL")
    return value.rstrip("/")


@dataclass(frozen=True)
class Settings:
    stt_base_url: str
    stt_model: str
    stt_api_key: str | None
    nvidia_base_url: str
    nvidia_api_key: str
    nvidia_model: str
    elevenlabs_api_key: str
    elevenlabs_voice_id: str
    elevenlabs_model: str
    audio_sample_rate: int
    log_path: Path

    @classmethod
    def from_env(cls) -> Settings:
        stt_url = _base_url(
            "ACE_STT_BASE_URL", _required("ACE_STT_BASE_URL")
        )
        nvidia_url = _base_url(
            "ACE_NVIDIA_BASE_URL",
            os.environ.get(
                "ACE_NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1"
            ),
        )
        try:
            sample_rate = int(os.environ.get("ACE_AUDIO_SAMPLE_RATE", "16000"))
        except ValueError as exc:
            raise ValueError("ACE_AUDIO_SAMPLE_RATE must be an integer") from exc
        if sample_rate < 8000 or sample_rate > 48000:
            raise ValueError("ACE_AUDIO_SAMPLE_RATE must be between 8000 and 48000")

        stt_api_key = os.environ.get("ACE_STT_API_KEY", "").strip()
        return cls(
            stt_base_url=stt_url,
            stt_model=_required("ACE_STT_MODEL"),
            stt_api_key=stt_api_key or None,
            nvidia_base_url=nvidia_url,
            nvidia_api_key=_required("ACE_NVIDIA_API_KEY"),
            nvidia_model=_required("ACE_NVIDIA_MODEL"),
            elevenlabs_api_key=_required("ACE_ELEVENLABS_API_KEY"),
            elevenlabs_voice_id=_required("ACE_ELEVENLABS_VOICE_ID"),
            elevenlabs_model=(
                os.environ.get("ACE_ELEVENLABS_MODEL", "").strip()
                or "eleven_turbo_v2_5"
            ),
            audio_sample_rate=sample_rate,
            log_path=Path(os.environ.get("ACE_LOG_PATH", "logs/sessions.jsonl")),
        )
