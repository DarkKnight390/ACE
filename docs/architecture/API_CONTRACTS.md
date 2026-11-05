# ACE Shared API Contracts

**Status:** Proposed integration contract; endpoints are not implemented by this prototype.

**Last updated:** 2026-11-04

These contracts are framework-neutral. Team B must not import `ace_voice` internals. The authenticated business platform is the source of truth for users, businesses, agent configuration, conversation history, and analytics.

## Common requirements

- HTTPS in deployed environments.
- User-facing requests use the platform's authenticated user token. Service-to-service calls use short-lived workload credentials.
- The platform derives `business_id` and permissions from the principal and checks every requested resource against that identity. A body/path ID is not authorization.
- Runtime-to-platform calls use scoped service credentials, tenant context, trace IDs, and request timeouts.
- IDs are opaque strings (UUID recommended); timestamps are RFC 3339 UTC.
- JSON errors use `application/problem+json` (RFC 9457 shape): `type`, `title`, `status`, optional `detail`, `instance`, and extension fields `code` and `trace_id`.
- Never return provider secrets, internal stack traces, or unredacted credentials.

## Authentication and identity

Required claims/attributes: stable `sub`, authenticated principal type, allowed business/tenant IDs, roles/scopes, and token expiry. User-facing APIs require business membership and operation-specific role checks. Internal runtime APIs require a workload identity with least-privilege scopes such as `agent-config:read`, `conversation:write`, or `business-tool:execute`.

The voice runtime must obtain authoritative business and agent configuration from a platform service. It must not accept an arbitrary caller-supplied `business_id` as proof of tenancy. Development-only local execution may use explicitly configured test context; it is not an authentication implementation.

## Agent configuration supplied to runtime

**Owner:** Team B. **Consumer:** Team A.

`GET /internal/v1/businesses/{business_id}/voice-agents/{agent_id}/runtime-config`

Request: workload identity and `If-None-Match` (optional).

`200 application/json`:

```json
{
  "business_id": "biz_123",
  "agent_id": "agent_456",
  "version": 7,
  "active": true,
  "display_name": "Reception",
  "system_instructions": "Answer using the approved business information.",
  "greeting": "Hello, how can I help?",
  "language": "en",
  "voice": {"provider": "elevenlabs", "voice_id": "configured-voice"},
  "capabilities": ["availability.read", "booking.create"],
  "updated_at": "2026-11-04T12:00:00Z"
}
```

The response contains configuration only, not provider API keys. `404` represents an unavailable resource; `403` represents a scope/tenant denial; `409` can indicate an inactive or incompatible configuration. Configuration versions are immutable identifiers for audit and cache invalidation.

## Conversation session lifecycle

**Owner:** Team A runtime; Team B consumes events/history through the agreed platform boundary.

`POST /v1/voice/sessions`

Request:

```json
{
  "agent_id": "agent_456",
  "channel": "web_voice",
  "external_reference": "optional-provider-call-id"
}
```

`business_id` is derived from the authenticated identity/configuration lookup. A service caller cannot use this endpoint to start a session in another tenant.

`201 application/json`:

```json
{
  "session_id": "sess_789",
  "business_id": "biz_123",
  "agent_id": "agent_456",
  "agent_config_version": 7,
  "status": "active",
  "created_at": "2026-11-04T12:00:00Z"
}
```

`POST /v1/voice/sessions/{session_id}/turns` accepts `{"text":"..."}` for text-capable clients. Its response is a stream of UTF-8 NDJSON events (`application/x-ndjson`):

```json
{"type":"response.text.delta","session_id":"sess_789","sequence":1,"text":"Welcome"}
{"type":"response.text.delta","session_id":"sess_789","sequence":2,"text":"."}
{"type":"response.completed","session_id":"sess_789","turn_id":"turn_012"}
```

Errors before stream establishment use the common problem response. After establishment, stream errors use `{"type":"error","code":"...","trace_id":"..."}` and the server closes the stream. Clients must treat an interrupted stream as incomplete.

### Audio WebSocket

`wss://{host}/v1/voice/sessions/{session_id}/stream` authenticates with the platform-approved WebSocket credential mechanism; never put long-lived bearer tokens in query strings.

Client sends JSON `audio.start` with `encoding` (`pcm_s16le`), `sample_rate_hz`, and `channels`; then binary audio frames; then JSON `audio.end`. Server sends ordered JSON events (`transcript.partial`, `transcript.final`, `response.text.delta`, `response.completed`, `session.state`, `tool.started`, `tool.completed`, `error`) and binary PCM audio frames announced by `response.audio.start` with encoding/rate/channels/sequence. Every event is scoped to the authenticated session and includes a monotonically increasing sequence. Cancellation/close must stop model and TTS work and reject stale output.

## Tool execution

**Caller:** Team A. **Owner:** Team B business platform. No arbitrary code execution or direct database access.

`POST /internal/v1/businesses/{business_id}/tools/{tool_name}:execute`

Required headers: workload authorization, `Idempotency-Key`, `X-Trace-Id`.

Request:

```json
{
  "session_id": "sess_789",
  "agent_id": "agent_456",
  "agent_config_version": 7,
  "tool_call_id": "toolcall_001",
  "arguments": {"service_id": "service_1", "requested_at": "2026-11-05T15:00:00Z"}
}
```

`200 application/json`:

```json
{
  "tool_call_id": "toolcall_001",
  "status": "succeeded",
  "result": {"available": true, "slot_id": "slot_2"}
}
```

Business authorization, argument validation, idempotency, and audit records are enforced by the platform. Expected tool failures use a typed result or common problem response. Mutating operations must not be retried without idempotency semantics.

## Conversation and call history

**Owner:** Team B for durable records and user-facing APIs; Team A emits normalized events.

Proposed user-facing endpoint: `GET /v1/businesses/{business_id}/conversations?cursor={opaque}&limit={1..100}`. It returns only records visible to that user's authorized business:

```json
{
  "items": [{
    "conversation_id": "sess_789",
    "channel": "phone",
    "status": "completed",
    "started_at": "2026-11-04T12:00:00Z",
    "ended_at": "2026-11-04T12:04:00Z",
    "agent_id": "agent_456",
    "outcome": "booking_created",
    "summary": null,
    "recording": null
  }],
  "next_cursor": null
}
```

Transcript, summary, customer identity, recording URL, and retention metadata are optional, permission-controlled fields. Recording is absent unless separately authorized and consent/retention requirements are met. Do not present mock history as production data.

## Usage and analytics events

Team A emits versioned, idempotent events with `event_id`, `event_type`, `occurred_at`, `business_id`, `agent_id`, `session_id`, optional `turn_id`, and `schema_version`. Initial event types: `conversation.started`, `conversation.ended`, `turn.completed`, `tool.completed`, and `usage.recorded`. Usage records identify measurable units (duration, tokens where reported, audio seconds), provider/model identifiers, and source timestamps. Do not include raw audio, credentials, or transcript text in analytics payloads. Team B validates, deduplicates, stores, and exposes authorized reporting.

## Versioning and change process

Additive optional fields are compatible within a version. Breaking changes require a new version and an entry in `docs/agents/INTEGRATION_LOG.md` with owner, migration/compatibility plan, and approval before either team implements against the changed contract.
