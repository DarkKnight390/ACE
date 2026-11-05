# ACE — Automated Communication Engine

ACE is a modular platform for AI-powered business conversations. Team A owns the voice and intelligence runtime; Team B owns the business platform and dashboard. See [AGENTS.md](./AGENTS.md) and the [architecture documents](./docs/architecture/SYSTEM_ARCHITECTURE.md) before changing shared interfaces.

## Current state

The repository currently contains the initial architecture/contracts and a local, CLI-first voice prototype. It records microphone audio, transcribes locally with Faster-Whisper, streams text from NVIDIA, speaks complete phrases through ElevenLabs PCM streaming, and keeps context for the active process. It does not yet include a web UI, telephony provider, or production authentication.

## Setup

Requires Python 3.11+, a microphone and speakers/headphones. From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[audio,test]"
Copy-Item .env.example .env
```

Configure speech recognition and set the provider credentials in `.env`:

- `ACE_STT_MODEL` selects the local Faster-Whisper model (default `small`); its weights download on first transcription.
- `ACE_STT_DEVICE` and `ACE_STT_COMPUTE_TYPE` default to `cpu` and `int8`. Set `ACE_STT_LANGUAGE` to an ISO language code to disable language detection; leave it empty for automatic detection.
- `ACE_NVIDIA_API_KEY` and `ACE_NVIDIA_MODEL` configure NVIDIA's chat-completions API.
- `ACE_ELEVENLABS_API_KEY` and `ACE_ELEVENLABS_VOICE_ID` configure ElevenLabs.

The application reads environment variables; it does not automatically load `.env`. In PowerShell, load it in your terminal or use your preferred environment manager. Do not commit credentials.

## Run and test

```powershell
ace-voice
python -m unittest discover -s tests -v
```

Press Enter to finish each captured utterance. The assistant response is printed as it streams and played as PCM audio. Session logs contain event metadata and character counts, not transcripts. The log path is configurable with `ACE_LOG_PATH`.

See [Team A notes](./docs/agents/AGENT_A_NOTES.md) for verified scope, tests, limitations, and next steps; see [API contracts](./docs/architecture/API_CONTRACTS.md) for the planned Team B integration boundary.
