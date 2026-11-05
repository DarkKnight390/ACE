# Team B Onboarding Notes

**Status:** Assignment and onboarding guidance only. No Team B implementation is represented here.

## Mission

Build the ACE Business Platform: authentication and business identity, tenant onboarding/configuration, agent management, dashboard/frontend, business data, conversation history, and analytics presentation. Team B owns its internal architecture and frontend; it does not own the Team A voice runtime.

## First steps

1. Inspect the repository, current branch, and `AGENTS.md` before changing files.
2. Review [SYSTEM_ARCHITECTURE.md](../architecture/SYSTEM_ARCHITECTURE.md), [API_CONTRACTS.md](../architecture/API_CONTRACTS.md), and [DATABASE_SCHEMA.md](../architecture/DATABASE_SCHEMA.md).
3. Confirm the frontend/backend framework and database before adding dependencies; the existing repository did not contain these choices at initial inspection.
4. Own implementation under the business-platform paths selected by Team B. Do not edit `src/ace_voice/` or Team A-owned tests.
5. Implement the API contracts without importing Team A internals. Resolve disagreements through the integration log before changing shared interfaces.
6. Add Team B-specific tests, setup instructions, and an implementation note before committing related changes.

## Team B scope

- Authentication, membership, business creation, and tenant authorization.
- Business profile, operating hours, services, and business-owned configuration.
- Agent configuration authoring/versioning and an authorized runtime configuration API.
- Conversation/call history, reporting/analytics, and any dashboard UI.
- Platform-side tool execution, permission checks, idempotency, and audit records.
- Durable database schema, migrations, retention, and privacy controls.

## Integration boundary

Team B exposes the versioned contracts in `docs/architecture/API_CONTRACTS.md`. The voice runtime receives configuration through an authenticated service API and reports normalized session/usage events through the agreed contract. Business IDs in client requests are not authorization. Keep credentials server-side and never expose provider keys to a browser.

## Coordination

Record proposed shared API/schema changes in `docs/agents/INTEGRATION_LOG.md` with the affected contract, rationale, compatibility plan, and decision. Do not assume a proposed contract is already deployed or an API response is available until both sides verify it.
