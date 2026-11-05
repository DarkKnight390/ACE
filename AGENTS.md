# ACE Development Instructions

## Project and ownership

- ACE is developed as a modular, API-first communication platform.
- Team A owns `src/ace_voice/`, its tests, and voice-runtime documentation.
- Team B owns the business platform, dashboard, tenant administration, and business data.
- Shared API and persistence changes must be documented and coordinated in `docs/agents/INTEGRATION_LOG.md` before implementation.
- Do not import Team B's internal modules or write directly to its database.
- Preserve existing work and follow the current feature branch. Do not push directly to `main` or merge into the integration branch.

## Engineering rules

- Keep provider-specific behavior inside `src/ace_voice/providers/`; depend on typed ports elsewhere.
- Keep secrets in environment variables. Never commit `.env` or credentials.
- Use asynchronous network operations and propagate failures; do not hide provider errors behind empty or success-shaped responses.
- Keep session logs structured and avoid writing conversation content or credentials by default.
- Add or update tests and `docs/agents/AGENT_A_NOTES.md` for every meaningful Team A implementation.
- Do not claim a feature, test, commit, or push completed until it has been verified.

## Local development

- Python 3.11 or newer is the intended baseline.
- Install the project with `python -m pip install -e ".[audio]"`; use `.[test]` for tests.
- Copy `.env.example` to `.env` and supply credentials/configuration locally.
- Run the local prototype with `ace-voice`.
- Run tests with `python -m unittest discover -s tests -v`.

The local CLI prototype is intentionally separate from Team B's frontend. Deployment API and authentication choices remain subject to the contracts in `docs/architecture/API_CONTRACTS.md`.
