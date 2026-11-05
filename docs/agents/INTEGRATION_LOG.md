# ACE Integration Log

Use this log for shared API, event, and persistence decisions. A proposal is not an implemented or approved integration. Record a decision before either team builds against a breaking change.

## 2026-11-04 — Initial contract baseline (proposed)

- **Status:** Proposed; Team B has not implemented the interfaces.
- **Decision area:** Authentication, runtime agent configuration, conversation sessions/streams, business tool execution, history, and usage events.
- **Details:** See `docs/architecture/API_CONTRACTS.md`. Team B remains the source of truth for business identity/configuration/history; Team A consumes versioned APIs and emits runtime events. No direct database access between teams.
- **Database:** PostgreSQL is a recommendation only. No database or schema has been selected or introduced.
- **Action required:** Team B review and acceptance; jointly select authentication/workload identity and transport details before deployment.
