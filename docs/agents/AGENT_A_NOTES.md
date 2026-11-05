# Team A Implementation Notes

## 2026-11-04 — Initial architecture and local voice prototype

- **Implemented:** Established Team A ownership/development rules and architecture/API/database proposals. Added typed provider/audio/tool/telephony ports; configurable OpenAI-compatible STT, NVIDIA streaming chat, and ElevenLabs PCM streaming adapters; in-memory conversation context; phrase segmentation; metadata-only JSONL session logging; and a local microphone/playback CLI.
- **Why:** Create a replaceable, testable first voice path while keeping Team B's platform and durable data ownership outside the voice runtime.
- **Files created or modified:** `AGENTS.md`, `README.md`, `.gitignore`, `.env.example`, `pyproject.toml`; `src/ace_voice/{__init__.py,config.py,models.py,ports.py,phrase_segmenter.py,session_log.py,audio.py,cli.py}`; `src/ace_voice/conversation/{__init__.py,engine.py}`; `src/ace_voice/providers/{__init__.py,nvidia.py,openai_compatible_stt.py,elevenlabs.py}`; `tests/{test_audio.py,test_engine.py,test_phrase_segmenter.py,test_providers.py}`; `docs/architecture/{SYSTEM_ARCHITECTURE.md,API_CONTRACTS.md,DATABASE_SCHEMA.md}`; `docs/agents/{AGENT_A_NOTES.md,AGENT_B_NOTES.md,INTEGRATION_LOG.md}`; and status updates to `docs/roadmap/{MASTER_ROADMAP.md,TEAM_A_ROADMAP.md,TEAM_B_ROADMAP.md}`.
- **Dependencies introduced:** `httpx` required; `sounddevice` optional for local capture/playback. No FastAPI, database driver, telephony SDK, or local ASR model was added.
- **API/interface changes:** Added internal typed ports and proposed Team B-facing REST/WebSocket, agent-config, tool-execution, history, and usage-event contracts. No network service API has been implemented.
- **Tests performed and results:** `python -m pip install -e ".[audio,test]"` succeeded on Python 3.14.6. `python -m unittest discover -s tests -v` passed all 8 tests, including mocked NVIDIA/ElevenLabs/STT streams, audio WAV/PCM framing, phrase segmentation, conversation context, and log redaction. `python -m compileall -q src tests` succeeded. Live microphone, speaker, and provider credentials were not exercised.
- **Known limitations:** STT requires an operator-provided OpenAI-compatible transcription endpoint; live hardware and provider credentials have not been verified. The CLI has no web UI, authentication, VAD, barge-in, cancellation, retries, tool execution, telephony, persistent sessions, or production analytics. Model generation currently pauses while each phrase is synthesized/played.
- **Next implementation task:** Perform a live local smoke test with configured credentials and hardware, then implement overlapping LLM/TTS streaming and cancellation in the next Team A iteration.

## Post-commit follow-up — 2026-11-04

- **Local commit:** `ecff3cc` (`feat: establish ACE voice engine foundation`).
- **Push status:** `git push -u origin team-a/voice-engine-foundation` was attempted and failed because no GitHub credentials are available in this environment. The feature branch is local and is not published.
- **Next action:** Configure Git Credential Manager or SSH authentication in the development environment, then push this branch and record the successful push.

## Post-push follow-up — 2026-11-04

- **Published branch:** `team-a/voice-engine-foundation`.
- **Pushed commit:** `f69c911791b887b5fb4d84ffeee5a2f024421835` (`docs: record initial milestone push status`), including the foundation commit `ecff3cc`.
- **Push status:** Verified; `HEAD` matches `origin/team-a/voice-engine-foundation`.

## 2026-11-04 — Switch local STT to Faster-Whisper

- **Implemented:** Replaced the remote OpenAI-compatible transcription adapter with a local Faster-Whisper adapter. Model loading is lazy and cached; synchronous inference runs off the asyncio event loop. Added configurable model, device, compute type, and optional language, defaulting to `small`/`cpu`/`int8` with automatic language detection.
- **Why:** Use the requested local speech recognizer and remove the STT API endpoint/key dependency from the prototype.
- **Files created or modified:** `pyproject.toml`, `.env.example`, `README.md`, `src/ace_voice/config.py`, `src/ace_voice/cli.py`, `src/ace_voice/providers/faster_whisper.py`; removed `src/ace_voice/providers/openai_compatible_stt.py`; updated `tests/test_providers.py`, added `tests/test_config.py`, and revised `docs/architecture/SYSTEM_ARCHITECTURE.md` and `docs/roadmap/TEAM_A_ROADMAP.md`. Updated ignored local `.env` STT settings without changing other configuration values.
- **Dependencies introduced:** `faster-whisper>=1.1,<2` in the optional `audio` extra; its model weights are downloaded on first use.
- **API/interface changes:** The internal `SpeechRecognizer` port remains unchanged. STT configuration now uses `ACE_STT_MODEL`, `ACE_STT_DEVICE`, `ACE_STT_COMPUTE_TYPE`, and optional `ACE_STT_LANGUAGE`; STT endpoint and API key settings are no longer used.
- **Tests performed and results:** `python -m pip install -e ".[audio,test]"` succeeded with Faster-Whisper 1.2.1 installed. `python -m unittest discover -s tests -v` passed all 11 tests. `python -m compileall -q src tests` and `python -m pip check` succeeded. Pylance diagnostics for the changed adapter, CLI, config, and provider tests reported no issues after correction.
- **Known limitations:** Real speech accuracy/performance and model download have not been tested end-to-end. Default CPU `int8` trades some speed/precision for broad hardware compatibility; CUDA or another model/compute type may be configured.
- **Next implementation task:** Run the full test suite and editable install with audio extras; perform a local microphone/model smoke test when model download and hardware are available.
