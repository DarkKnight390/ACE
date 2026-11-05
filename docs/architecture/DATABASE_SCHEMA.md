# ACE Database Schema and Ownership

**Status:** Proposal only; this project has no database connection or migrations.

**Last updated:** 2026-11-04

## Ownership

- Team B owns the business platform's durable source of truth, schema, migrations, tenant isolation, user/business identity, agent configuration, conversation history, usage reporting, and retention.
- Team A owns runtime session objects and emits versioned lifecycle/usage events. The initial prototype holds conversation context in memory and writes local metadata-only JSONL logs; neither is a production database.
- Team A must not connect directly to or create migrations in Team B's database. Runtime integration is through authenticated APIs and/or agreed events.
- A PostgreSQL-compatible platform database is a reasonable default if no existing database has been selected. Confirm the existing platform and operational requirements before choosing a driver or adding migrations.

## Proposed logical entities

These entities are a contract-planning aid, not implemented tables. Names/types should be adapted to Team B's existing conventions before implementation.

| Entity | Owner | Key fields and constraints |
|---|---|---|
| `businesses` | B | `id`, status, locale/timezone, timestamps |
| `users` | B | `id`, external identity subject, status; authentication provider owns credentials |
| `business_memberships` | B | `business_id`, `user_id`, role; unique pair and tenant-scoped authorization |
| `voice_agents` | B | `id`, `business_id`, active status, current config version |
| `voice_agent_versions` | B | `agent_id`, immutable version, instructions/configuration, author and timestamp |
| `conversation_sessions` | B | `id`, `business_id`, `agent_id`, config version, channel, status, started/ended timestamps, outcome |
| `conversation_turns` | B | `id`, `session_id`, sequence, direction, timestamps, transcript/summary subject to retention and access policy |
| `tool_executions` | B | `id`, session/turn IDs, tool name, idempotency key, status, timestamps, redacted result/error metadata |
| `usage_events` | B | unique event ID, business/session/agent IDs, unit, quantity, provider/model, occurred timestamp |
| `audit_events` | B | actor/workload, tenant, action, resource, timestamp, trace ID; no secrets |
| `recording_assets` | B | restricted object reference, consent/retention/access metadata; never store raw audio in a general-purpose row |

## Integrity and access recommendations

- Tenant-owned records include a non-null `business_id` directly or are enforced through a constrained parent relationship; queries and authorization are tenant-scoped.
- Use foreign keys and stable opaque IDs. Use uniqueness constraints for `(agent_id, version)`, `(session_id, sequence)`, and event/idempotency identifiers where applicable.
- Index tenant and time access patterns, such as `(business_id, started_at DESC)` for history and `(business_id, occurred_at)` for usage.
- Keep immutable agent configuration versions so a conversation can identify the configuration it used.
- Store event metadata and minimal transcript content only as required. Define retention, deletion, consent, encryption, and recording authorization before storing audio or transcripts.
- Do not persist provider credentials in configuration tables. Reference a managed secret identifier if a future provider credential must be tenant-configurable.

## Runtime data lifecycle

1. The runtime authenticates to the platform and resolves the authorized business/agent configuration version.
2. The runtime maintains active turn context transiently and sends normalized lifecycle/usage events through the agreed integration boundary.
3. The platform validates tenant scope, deduplicates events, and writes durable records.
4. The dashboard reads business history and analytics from authorized platform APIs, never from Team A process memory.

No SQL schema, migration, or database dependency is part of the current milestone.
