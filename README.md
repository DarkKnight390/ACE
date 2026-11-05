# ACE — Automated Communication Engine

ACE is a modular platform for AI-powered business conversations. Team A owns the voice and intelligence runtime; Team B owns the business platform and dashboard. See [AGENTS.md](./AGENTS.md) and the [architecture documents](./docs/architecture/SYSTEM_ARCHITECTURE.md) before changing shared interfaces.

## Current state

The repository currently contains the initial architecture/contracts and a local, CLI-first voice prototype. It records microphone audio, submits it to a configurable OpenAI-compatible transcription endpoint, streams text from NVIDIA, speaks complete phrases through ElevenLabs PCM streaming, and keeps context for the active process. It does not yet include a web UI, telephony provider, or production authentication.

## Setup

Requires Python 3.11+, a microphone and speakers/headphones. From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[audio,test]"
Copy-Item .env.example .env
```

Set the endpoint, model, and credentials in `.env`:

- `ACE_STT_BASE_URL`, `ACE_STT_MODEL`, and optionally `ACE_STT_API_KEY` must target an OpenAI-compatible `/audio/transcriptions` endpoint returning `{"text":"..."}`.
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
