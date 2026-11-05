# ACE — TEAM B DEVELOPMENT ROADMAP

**Team:** B  
**Ownership:** Business Platform and SaaS Application  
**Primary responsibility:** Business onboarding, configuration, management and reporting.

## CURRENT PROJECT STATUS — 2026-11-04

- No Team B application or backend implementation was present at initial inspection.
- Team B scope and onboarding instructions are in `docs/agents/AGENT_B_NOTES.md`; shared interfaces are proposals in `docs/architecture/API_CONTRACTS.md`.
- No Team B work is marked complete. Review and agreement on authentication, business configuration, event ingestion, and persistence are required before production integration.

## PHASE B0 — APPLICATION ARCHITECTURE

### Objectives

Establish the business-facing application architecture.

### Implementation tasks

1. Inspect the existing repository and frontend framework.
2. Establish frontend structure.
3. Establish design conventions.
4. Define navigation architecture.
5. Define authentication requirements.
6. Define tenant and business models.
7. Define agent configuration models.
8. Define dashboard API interfaces.
9. Establish reusable UI components.
10. Establish frontend testing.

### Deliverables

- Functional application shell.
- Navigation.
- Design system foundation.
- API client structure.
- Authentication and business-context plan.

## PHASE B1 — BUSINESS ONBOARDING

### Objectives

Allow businesses to create accounts and configure their organisation.

### Implementation tasks

1. Account registration.
2. Login.
3. Password recovery.
4. Business creation.
5. Business profile configuration.
6. Business name and contact information.
7. Business category selection.
8. Business address and timezone.
9. Operating hours.
10. Service and department configuration.
11. Business onboarding progress.
12. Business settings.

### Deliverables

A business can register and complete its initial setup.

## PHASE B2 — AI AGENT MANAGEMENT

### Objectives

Allow businesses to create and configure their AI agents.

### Implementation tasks

1. Agent creation.
2. Agent naming.
3. Agent description.
4. Agent role selection.
5. Personality configuration.
6. Custom instructions.
7. Greeting configuration.
8. Voice selection.
9. Language configuration.
10. Response style configuration.
11. Agent activation and deactivation.
12. Agent testing interface.
13. Agent configuration versioning.

### Initial agent templates

- Receptionist.
- Customer support agent.
- Booking assistant.
- Sales enquiry assistant.
- Construction enquiry assistant.
- General business assistant.

Templates must be configurable, not hardcoded as separate applications.

### Deliverables

Businesses can create, configure and manage multiple AI agents.

## PHASE B3 — BUSINESS KNOWLEDGE MANAGEMENT

### Objectives

Allow businesses to teach their agents about their operations.

### Implementation tasks

1. Knowledge-base management.
2. Business information editor.
3. FAQ management.
4. Service catalogue.
5. Product information.
6. Pricing information.
7. Operating policies.
8. Document uploads.
9. Knowledge-source management.
10. Document processing status.
11. Knowledge update management.
12. Source deletion and retention controls.

### Deliverables

Businesses can maintain their information and configure what their AI agents are allowed to use.

## PHASE B4 — CUSTOMER AND CONVERSATION MANAGEMENT

### Objectives

Give businesses visibility into their AI interactions.

### Implementation tasks

1. Conversation history.
2. Call history.
3. Customer profiles.
4. Customer contact information.
5. Conversation transcripts.
6. Call summaries.
7. Interaction timestamps.
8. Call outcomes.
9. Unanswered and failed interactions.
10. Escalated interactions.
11. Search and filtering.
12. Interaction details.

### Privacy requirements

- Tenant isolation.
- Role-based access.
- Recording access restrictions.
- Configurable retention.
- Appropriate disclosure and consent controls.

### Deliverables

Businesses can inspect and manage their customer interactions.

## PHASE B5 — APPOINTMENTS AND BUSINESS OPERATIONS

### Objectives

Give businesses tools to manage actions performed by ACE.

### Implementation tasks

1. Appointment dashboard.
2. Booking management.
3. Customer enquiry management.
4. Availability views.
5. Appointment status.
6. Rescheduling interface.
7. Cancellation interface.
8. Staff assignment.
9. Human escalation inbox.
10. Manual interaction management.
11. Operational notifications.
12. Business workflow settings.

### Deliverables

Business owners can manage the operational activities initiated by ACE.

## PHASE B6 — TELEPHONY AND CHANNEL MANAGEMENT

### Objectives

Allow businesses to configure their communication channels.

### Implementation tasks

1. Phone-number configuration interface.
2. Incoming-call settings.
3. Outbound-call settings.
4. Call routing.
5. Business greeting configuration.
6. Human handover configuration.
7. Call transfer settings.
8. Hold preferences.
9. Communication channel management.
10. Channel activation status.
11. Provider configuration status.
12. Call usage display.

### Future channel support

- Telephone.
- WhatsApp.
- SMS.
- Website voice.
- Website chat.
- Instagram messaging.

Do not build provider integrations that Team A has not exposed through agreed interfaces.

### Deliverables

Businesses can configure their available communication channels.

## PHASE B7 — ANALYTICS AND REPORTING

### Objectives

Show businesses the value ACE delivers.

### Implementation tasks

1. Total interactions.
2. Calls answered.
3. Missed calls.
4. Average response time.
5. Conversation duration.
6. Successful bookings.
7. Enquiries captured.
8. Escalated interactions.
9. Failed interactions.
10. Agent performance.
11. Usage statistics.
12. Cost and usage summaries where available.
13. Date-based reporting.
14. Exportable reports.

### Deliverables

A meaningful business analytics dashboard based on verified platform events.

## PHASE B8 — SUBSCRIPTIONS AND COMMERCIAL MANAGEMENT

### Objectives

Prepare ACE for commercial subscriptions.

### Implementation tasks

1. Subscription plans.
2. Plan selection.
3. Usage allowances.
4. Usage limits.
5. Billing integration.
6. Payment status.
7. Subscription renewal.
8. Plan upgrades.
9. Plan downgrades.
10. Usage notifications.
11. Invoice history.
12. Account suspension and restoration rules.

Billing must use verified usage events from the backend. Do not calculate charges from unverified frontend values.

### Deliverables

A business can subscribe to ACE and monitor its usage and billing.

## PHASE B9 — ORGANISATION AND ADMINISTRATION

### Objectives

Support businesses with multiple staff members and administrative needs.

### Implementation tasks

- Organisation management.
- Staff invitations.
- Role-based permissions.
- Team access.
- Agent assignment.
- Business-level permissions.
- Account security.
- Audit history.
- Administrative controls.
- Customer support workflows.

### Deliverables

A scalable organisation and account-management system.

## PHASE B10 — PRODUCTION READINESS AND USER EXPERIENCE

### Objectives

Prepare the platform for real customers.

### Implementation tasks

- Responsive interface.
- Accessibility.
- Form validation.
- Error states.
- Loading states.
- Empty states.
- Notification system.
- API error recovery.
- Authentication hardening.
- Permission testing.
- Tenant-isolation testing.
- Performance optimisation.
- Frontend automated testing.
- User onboarding improvements.
- Deployment configuration.

### Final deliverable

A complete business-facing ACE application that can configure and manage the ACE Voice & Intelligence Engine.

## TEAM B COMPLETION REQUIREMENTS

AGENT_B_NOTES.md must be updated after each meaningful implementation and included in the corresponding commit.

All controls must perform real actions or be clearly marked as unavailable or mock functionality.

Never present mock analytics, bookings or call records as verified production data.