from __future__ import annotations

import asyncio
import logging
import sys

import httpx

from ace_voice.audio import LocalAudioIO
from ace_voice.config import Settings
from ace_voice.conversation.engine import VoiceConversationEngine
from ace_voice.models import ConversationSession, Message
from ace_voice.providers.elevenlabs import ElevenLabsTextToSpeech
from ace_voice.providers.faster_whisper import FasterWhisperSpeechRecognizer
from ace_voice.providers.nvidia import NvidiaLanguageModel
from ace_voice.session_log import JsonlSessionLogger


async def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    settings = Settings.from_env()
    timeout = httpx.Timeout(connect=10.0, read=90.0, write=30.0, pool=10.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        recognizer = FasterWhisperSpeechRecognizer(
            model_size=settings.stt_model,
            device=settings.stt_device,
            compute_type=settings.stt_compute_type,
            language=settings.stt_language,
        )
        language_model = NvidiaLanguageModel(
            client,
            base_url=settings.nvidia_base_url,
            api_key=settings.nvidia_api_key,
            model=settings.nvidia_model,
        )
        text_to_speech = ElevenLabsTextToSpeech(
            client,
            api_key=settings.elevenlabs_api_key,
            voice_id=settings.elevenlabs_voice_id,
            model=settings.elevenlabs_model,
        )
        audio_io = LocalAudioIO(settings.audio_sample_rate)
        playback = audio_io.open_playback()
        logger = JsonlSessionLogger(settings.log_path)
        engine = VoiceConversationEngine(
            language_model, text_to_speech, logger
        )
        session = ConversationSession(
            messages=[
                Message(
                    role="system",
                    content=(
                        "You are ACE, a helpful business communication assistant. "
                        "Answer clearly and concisely. Do not claim to have completed "
                        "an action unless an approved tool confirms it."
                    ),
                )
            ]
        )
        print(f"ACE voice session: {session.session_id}", flush=True)

        def write_text(delta: str) -> None:
            sys.stdout.write(delta)
            sys.stdout.flush()

        try:
            while True:
                wav_audio = await asyncio.to_thread(audio_io.capture_until_enter)
                transcript = await recognizer.transcribe(wav_audio)
                if not transcript.strip():
                    print("No speech was recognized. Try again.", flush=True)
                    continue
                print(f"You: {transcript}", flush=True)
                print("ACE: ", end="", flush=True)
                await engine.respond(
                    session,
                    transcript,
                    on_text=write_text,
                    audio_sink=playback,
                )
                print("\n", flush=True)
        finally:
            await playback.close()


def run() -> None:
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nACE voice session ended.", flush=True)
