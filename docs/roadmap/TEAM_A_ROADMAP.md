# ACE — TEAM A DEVELOPMENT ROADMAP

**Team:** A  
**Ownership:** Voice & Intelligence Engine  
**Primary responsibility:** Real-time AI conversation and voice runtime.

## CURRENT PROJECT STATUS — 2026-11-04

- The initial local CLI milestone provides local Faster-Whisper speech transcription, NVIDIA streamed reasoning, phrase-based ElevenLabs PCM speech, local microphone/playback adapters, in-memory context, and metadata-only session logs.
- This is a development prototype, not a deployed service. Hardware/provider integration and its limitations are recorded in `docs/agents/AGENT_A_NOTES.md`.
- Next: verify this baseline, then improve overlapping generation/playback, cancellation, and failure handling before VAD/barge-in or telephony.

## PHASE A0 — VOICE ENGINE ARCHITECTURE

### Objectives

Establish the internal architecture before implementing individual providers.

### Implementation tasks

1. Create the voice-engine module structure.
2. Establish provider abstraction interfaces.
3. Define audio input and output interfaces.
4. Define speech-recognition interfaces.
5. Define language-model interfaces.
6. Define text-to-speech interfaces.
7. Define conversation session models.
8. Define event-driven communication.
9. Define tool execution interfaces.
10. Establish structured logging and error handling.

### Suggested module structure

- audio/
- speech/
- llm/
- tts/
- conversation/
- sessions/
- orchestration/
- tools/
- providers/
- events/
- monitoring/

Adapt this structure to the existing repository rather than duplicating existing modules.

### Deliverables

- Architecture documentation.
- Provider interface definitions.
- Session model.
- Event model.
- Initial tests.

## PHASE A1 — AUDIO INPUT AND SPEECH RECOGNITION

### Objectives

Allow ACE to receive and understand spoken language.

### Implementation tasks

1. Implement microphone input.
2. Implement audio capture.
3. Implement audio format validation.
4. Implement audio buffering.
5. Integrate a speech-to-text provider.
6. Evaluate local Whisper and supported API alternatives.
7. Implement transcription handling.
8. Implement partial transcription where supported.
9. Implement speech endpoint detection.
10. Implement transcription confidence and failure handling where available.

### Requirements

- Configurable audio input.
- Correct sample-rate handling.
- Clear microphone error reporting.
- Low-latency transcription.
- Support for natural speech.
- Provider-independent interfaces.

### Deliverables

A working speech-input pipeline that converts spoken language into usable conversation events.

## PHASE A2 — AI REASONING ENGINE

### Objectives

Connect ACE to NVIDIA AI models and build the reasoning layer.

### Implementation tasks

1. Create NVIDIA provider adapter.
2. Implement secure API configuration.
3. Implement model selection.
4. Implement streaming model requests.
5. Implement structured message handling.
6. Implement system instructions.
7. Implement conversation context.
8. Implement response cancellation.
9. Implement timeouts and retry policies.
10. Implement model error handling.
11. Implement usage tracking.
12. Evaluate alternative compatible models.

### Requirements

The model interface must not be permanently coupled to NVIDIA.

The system should be able to change models through configuration and provider adapters.

### Deliverables

A functional reasoning service capable of processing user requests and producing streaming responses.

## PHASE A3 — ELEVENLABS VOICE ENGINE

### Objectives

Convert AI-generated responses into natural speech.

### Implementation tasks

1. Create ElevenLabs provider adapter.
2. Implement API credential management.
3. Implement voice selection.
4. Implement voice configuration.
5. Implement text-to-speech generation.
6. Implement streaming TTS.
7. Implement audio chunk processing.
8. Implement playback buffering.
9. Implement audio playback.
10. Implement interrupted-generation cancellation.
11. Implement voice-generation error recovery.
12. Measure generation latency.

### Requirements

- Natural voice output.
- Configurable voice selection.
- Streaming audio generation.
- Efficient phrase segmentation.
- No unnecessary waiting for entire paragraphs.
- Replaceable TTS provider interface.

### Deliverables

A working text-to-speech pipeline capable of receiving streamed text and producing playable speech.

## PHASE A4 — REAL-TIME CONVERSATION ORCHESTRATOR

### Objectives

Connect all voice services into a coordinated conversation engine.

### Implementation tasks

1. Create conversation orchestrator.
2. Implement session lifecycle management.
3. Connect STT to the reasoning service.
4. Connect the reasoning service to TTS.
5. Implement event-driven processing.
6. Implement conversation history.
7. Implement turn management.
8. Implement streaming response segmentation.
9. Implement audio playback coordination.
10. Implement session termination and cleanup.
11. Implement concurrency-safe session handling.

### Progressive response generation

Implement a response pipeline that can:

- Begin generating a response.
- Identify natural phrase boundaries.
- Submit completed phrases to TTS.
- Receive audio chunks.
- Play audio progressively.
- Continue generating the remaining response.

Avoid sending incomplete or fragmented tokens directly to TTS.

### Deliverables

A working local AI voice conversation system.

## PHASE A5 — NATURAL CONVERSATION AND INTERRUPTION MANAGEMENT

### Objectives

Make ACE feel like a real-time conversational assistant.

### Implementation tasks

1. Voice activity detection.
2. Silence detection.
3. Speech endpoint detection.
4. Turn-taking management.
5. Barge-in detection.
6. Playback interruption.
7. Pending response cancellation.
8. Stale response protection.
9. Conversation context updates.
10. Handling simultaneous input and output.
11. Handling callers speaking while the AI speaks.
12. Recovery after interruptions.

### Deliverables

A voice engine capable of handling natural interruptions without continuing outdated responses.

## PHASE A6 — PROGRESSIVE RESPONSES AND WAITING MANAGEMENT

### Objectives

Make the AI responsive while it retrieves information or executes operations.

### Response types

1. Immediate acknowledgements.
2. Progress updates.
3. Final answers.
4. Clarification requests.
5. Error explanations.
6. Human escalation messages.

### Implementation tasks

- Create a response-state manager.
- Implement acknowledgement generation.
- Implement configurable progress messages.
- Implement progress-event handling.
- Implement long-running operation detection.
- Implement waiting intervals.
- Implement maximum waiting duration.
- Implement background tool execution.
- Implement recovery from failed operations.
- Prevent duplicate or misleading progress messages.

### Actual hold management

Separate conversational waiting from telephone hold.

Implement an abstract hold-state interface now.

Actual telephone hold, music and call-control operations will be implemented when the telephony adapter is available.

### Deliverables

ACE can continue a natural conversation while approved business operations execute.

## PHASE A7 — BUSINESS TOOL EXECUTION ENGINE

### Objectives

Give ACE the ability to perform actual business tasks.

### Implementation tasks

1. Create tool registry.
2. Define tool schemas.
3. Implement structured function calling.
4. Implement argument validation.
5. Implement permission checking.
6. Implement tool execution.
7. Implement tool result handling.
8. Implement execution timeouts.
9. Implement retries where safe.
10. Implement idempotency for actions.
11. Implement tool execution logs.
12. Implement human approval requirements for sensitive operations.

### Initial tools

- Check business information.
- Check availability.
- Retrieve service prices.
- Collect customer information.
- Create an appointment.
- Retrieve appointment details.
- Cancel or reschedule an appointment.
- Create an enquiry.
- Transfer a conversation to a human.

Do not allow the model to execute arbitrary code or unrestricted database queries.

### Deliverables

A controlled tool-execution system that allows ACE to complete approved business workflows.

## PHASE A8 — KNOWLEDGE AND CONTEXT INTEGRATION

### Objectives

Allow agents to retrieve relevant business information.

### Implementation tasks

- Business-specific context loading.
- Knowledge retrieval interfaces.
- Document retrieval integration.
- Context filtering by tenant.
- Relevant information selection.
- Conversation memory.
- Context-window management.
- Source tracking where applicable.
- Outdated information handling.

The business platform owns knowledge administration. Team A owns runtime retrieval and context integration.

### Deliverables

An agent can answer questions using the correct business's approved knowledge sources.

## PHASE A9 — TELEPHONY INTEGRATION

### Objectives

Prepare the voice engine for actual telephone calls.

### Implementation tasks

- Create telephony provider abstraction.
- Implement call-session adapter.
- Support telephone audio formats.
- Implement inbound call handling.
- Implement outbound call handling.
- Map call identifiers to conversation sessions.
- Implement call lifecycle events.
- Implement call termination.
- Implement hold-state operations.
- Implement human call transfer.
- Implement connection failure recovery.
- Implement recording integration where authorised.

Evaluate SIP, Twilio and Telnyx integrations.

Do not make provider-specific functionality a permanent dependency of the conversation engine.

### Deliverables

A voice engine that can receive and manage actual telephone conversations through a supported provider.

## PHASE A10 — PERFORMANCE, SECURITY AND PRODUCTION HARDENING

### Objectives

Prepare the engine for concurrent business usage.

### Implementation tasks

- Latency measurement.
- STT latency optimisation.
- Model time-to-first-token measurement.
- TTS time-to-first-audio measurement.
- End-to-end response latency measurement.
- Concurrent session testing.
- Memory and resource monitoring.
- Provider failure recovery.
- Rate limiting.
- Tenant-aware execution permissions.
- Secret management.
- Structured logs.
- Health checks.
- Monitoring.
- Automated integration tests.
- Load testing.

### Performance metrics

Track:

- Speech endpoint detection time.
- Transcription completion time.
- Model time to first token.
- Time to first complete spoken phrase.
- TTS time to first audio.
- Audio playback latency.
- End-to-end conversational response time.
- Tool execution duration.
- Session failure rate.

### Final deliverable

A stable, modular, independently deployable ACE Voice & Intelligence Engine.

## TEAM A COMPLETION REQUIREMENTS

Every implementation must be tested and documented.

AGENT_A_NOTES.md must be updated after each meaningful implementation and included in the corresponding commit.

Never mark a phase complete while critical functionality remains untested.