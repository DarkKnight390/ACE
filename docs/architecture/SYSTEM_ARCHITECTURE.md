# ACE System Architecture

**Status:** Initial proposal; no production deployment or shared database is present.

**Last updated:** 2026-11-04

## Design goals

- Keep conversation orchestration independent of AI, speech, audio, and telephony vendors.
- Keep Team A and Team B deployable independently and integrate only through versioned contracts.
- Resolve business and agent configuration through authorized platform APIs, never by importing Team B internals.
- Keep secrets server-side and tenant identity derived from authenticated credentials, not trusted from caller-supplied IDs.
- Start with a local voice prototype; add infrastructure only when an agreed runtime need exists.

## System boundaries

```text
Local microphone / future telephony
              |
       Audio input port
              |
   Conversation orchestrator
      |       |        |
      |       |        +-- approved business-tool port --> Team B API
      |       +----------- language-model port ----------> NVIDIA adapter
      +------------------- speech recognition port ------> configured STT adapter
              |
       text-to-speech port ------------------------------> ElevenLabs adapter
              |
       Audio output port --> local playback / future telephony
              |
       versioned session and event contracts <----------> Team B platform
```

### Team A — Voice & Intelligence Engine

Owns `src/ace_voice/`, voice session runtime, streaming orchestration, provider adapters, audio adapters, tool-execution client/guardrails, voice-specific tests, and runtime event production.

### Team B — Business Platform

Owns account authentication, business/tenant records, agent configuration authoring, dashboard/frontend, business data, conversation history presentation, analytics presentation, and platform-side implementations of the shared API contracts. Team B notes are onboarding instructions, not a claim of existing implementation.

### Shared boundary

Contracts are defined in [API_CONTRACTS.md](./API_CONTRACTS.md). Team A stores no business data and does not own Team B migrations. Changes to shared contracts or schema require an integration-log proposal and agreement before implementation.

## Replaceable provider ports

`src/ace_voice/ports.py` defines typed ports for:

- `SpeechRecognizer`: audio bytes to transcript.
- `LanguageModel`: asynchronous message-to-text-delta stream.
- `TextToSpeech`: phrase-to-audio-chunk stream.
- `AudioInput` and `AudioSink`: capture and output.
- `BusinessToolExecutor`: validated, authorized business operation.
- `TelephonyTransport`: audio receive/send and call termination.

The current adapters are NVIDIA chat completions, ElevenLabs PCM streaming, and a configurable OpenAI-compatible speech-to-text endpoint. Replacing a vendor should require a new adapter, not changes to conversation policy or session models.

## Initial local prototype

- `ace-voice` records one utterance at a time from the default microphone and encodes mono 16-bit WAV.
- A configurable `/audio/transcriptions` endpoint returns the transcript.
- The runtime appends the turn to in-memory session context and streams NVIDIA text.
- `PhraseSegmenter` yields sentence boundaries (or a bounded word boundary for long text); ElevenLabs returns PCM at 24 kHz and the local output adapter plays chunks as they arrive.
- JSONL session records contain event names, timestamps, IDs, and character counts only; transcript text is not logged.
- Context currently exists only in process memory. No authentication, multi-tenant persistence, VAD, barge-in, tools, or telephony is implemented.

## Technology recommendations

| Area | Initial recommendation | Current decision |
|---|---|---|
| Voice runtime | Python 3.11+ with typed async ports | Implemented for the local prototype |
| Provider HTTP | `httpx` asynchronous client | Implemented |
| Web/API edge | FastAPI after service auth and WebSocket framing are agreed | Deferred; no server API is needed by the CLI milestone |
| Speech recognition | Keep provider configurable behind the STT port; evaluate hosted and local options for latency, privacy, and cost | OpenAI-compatible transcription adapter implemented; endpoint/model supplied by the operator |
| NVIDIA reasoning | NVIDIA OpenAI-compatible chat completions behind an adapter | Implemented |
| Voice synthesis | ElevenLabs streaming API with PCM playback | Implemented |
| Local audio | `sounddevice` optional extra | Implemented as an optional local adapter |
| Database | PostgreSQL is a reasonable shared platform default if no compatible database exists | Not selected or introduced; Team B owns source-of-truth schema |
| Realtime transport | WebSocket with explicit audio/event framing | Contract documented; implementation deferred |
| Telephony | Vendor-neutral transport port; evaluate SIP and hosted providers after local prototype | Interface only |

No FastAPI, database driver, telephony SDK, or heavyweight local speech model is installed in this milestone. This avoids dependencies before authentication, ownership, provider costs, and deployment topology are agreed.

## Runtime and failure handling

- Provider HTTP status failures and malformed responses propagate to the caller; no retry or fallback can turn a failure into success.
- Provider calls have bounded connect/read/write timeouts at the CLI boundary.
- Provider secrets are read from environment variables and excluded from logs.
- Session logging is append-only JSONL for local diagnostics and is not durable production history.
- Provider retries, cancellation, idempotency, rate limits, concurrency controls, and health/usage telemetry are future work.

## Deployment evolution

1. Keep the current CLI as a development harness.
2. Add an authenticated FastAPI service only after the Team B service-to-service identity and session contracts are accepted.
3. Use WebSockets for framed audio and event streams; keep provider interfaces unchanged.
4. Persist business configuration and history through platform APIs/events owned by Team B.
5. Add telephony adapters without making call-provider identifiers the conversation-session identity.
