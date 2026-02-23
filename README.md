🌍 Project Vision

A safety-first multimodal assistive AI platform designed to empower individuals with physical and motor disabilities by enabling:

🎤 Hands-free system control

🧠 Context-aware decision making

🔒 Risk-controlled execution

🤝 Multimodal interaction (Voice → Gesture → Vision → Emotion)

⚙ Deterministic automation with confirmation safeguards

This system bridges the gap between human intent and digital control in real-world environments.

📂 Complete Project Structure
KRISHNA/
│
├── core/                          # Phase 1 — Intent & Safety Core
│   ├── __init__.py
│   ├── context_memory.py
│   ├── fusion_engine.py
│   ├── intent_parser.py
│   ├── intent_schema.py
│   ├── mode_manager.py
│   ├── safety_engine.py
│   ├── safety_rules.py
│   └── response_model.py          # UnifiedResponse
│
├── router/                        # Phase 3 — Decision Routing
│   └── decision_router.py
│
├── execution/                     # Phase 3.1 — Execution Engine
│   ├── execution_engine.py
│   ├── dispatcher.py
│   └── adapters/
│       ├── windows_app.py
│       ├── windows_browser.py
│       ├── windows_keyboard.py
│       ├── windows_file.py
│       └── windows_system.py
│
├── utility/                       # Phase 3.2 — Utility Engine
│   └── utility_engine.py
│
├── knowledge/                     # Phase 3.3 — Hybrid Knowledge
│   ├── knowledge_engine.py        # Wikipedia
│   └── llm_engine.py              # TinyLlama (Ollama)
│
├── voice/                         # Phase 2 + Phase 3.5 — Runtime
│   ├── assistant_runtime.py
│   ├── mic_stream.py
│   ├── vad.py
│   ├── stt.py
│   ├── tts.py
│   └── voice_loop.py
│
├── config.py
├── main.py
├── requirements.txt
├── README.md
│
├── tests/                         # Consolidated tests
│   ├── test_context.py
│   ├── test_parser.py
│   ├── test_safety.py
│   ├── test_execution.py
│   └── test_voice_pipeline.py
│
└── demos/
    ├── demo_phase2.py
    └── demo_full_pipeline.py

🏗 System Architecture
Voice / Gesture / Vision / Emotion
              ↓
        Intent Parser
              ↓
        Context Memory
              ↓
        Safety Engine
              ↓
        Fusion Engine
              ↓
        Execution Engine
              ↓
         User Feedback
Design Guarantees

Deterministic logic

Confirmation enforcement

Risk escalation handling

Single safe action execution

Real-time responsiveness

Accessibility-first design

🟢 PHASE 1 — Core Intent & Safety Engine

Status: ✅ Complete

🎯 Goal

Build a deterministic, safety-aware decision engine.

🔹 Components
Intent Schema

Structured Intent dataclass

Risk levels (0–9)

Confirmation flags

Entities & parameters

Session tracking

Intent Parser

Flexible keyword detection (anywhere in sentence)

Multi-word normalization ("shut down" → "shutdown")

Filler word removal

Target extraction

Structured parameter mapping

Supports:

Commands

Questions

Control instructions

Dictation mode

Unknown fallback

Mode Manager (Finite State Machine)

Modes:

LISTENING

COMMAND

DICTATION

QUESTION

DISABLED

Safety Engine

Risk scoring

Dangerous pattern escalation ("delete all")

Confirmation enforcement

Hard blocking for extreme risk

Context Memory

Multi-step linking

Confirmation retention

Session awareness

Fusion Engine

Combines parsing + safety + context

Handles confirmation state

Generates structured decision objects

Tracks latency

🧪 Phase 1 Testing
Test Type	Status
Command detection	✅
Risk escalation	✅
Confirmation loop	✅
Cancel flow	✅
Hard blocking	✅
Mode transitions	✅text
🎤 PHASE 2 — Real-Time Voice Integration

Status: ✅ Complete

🎯 Goal

Transform decision engine into real-time assistive voice system.

🔹 Technologies Used

faster-whisper (GPU accelerated STT)

PyTorch CUDA

WebRTC VAD

SoundDevice

PyTTSx3

NumPy

Threading

🔹 Components
Microphone Stream

16kHz fixed rate

30ms frames

Queue buffering

VAD compatible

Voice Activity Detection (WebRTC)

Balanced aggressiveness tuning

Silence detection

Minimum speech duration threshold

Noise robustness

Speech-to-Text

GPU acceleration

CPU fallback

Beam search optimization

Short audio rejection

Text-to-Speech

Non-blocking

Thread-safe

Offline capable

Real-Time Runtime

Speech segmentation

Silence-based stop logic

Noise filtering

Confirmation voice loop

🧪 Phase 2 Testing
Scenario	Result
Silence rejection	✅
Background noise filtering	✅
Natural language flexibility	✅
Confirmation handling	✅
Cancellation handling	✅
Latency stability	✅
🟢 PHASE 3 — Execution Engine

Status: 🟡 Execution Complete | Runtime Hardening Ongoing

🎯 Goal

Safely connect approved intents to real OS actions with confirmation, safety enforcement, and structured audit logging.

✅ Completed
1️⃣ Approved-Only Execution

ExecutionEngine runs only:

APPROVED intents
Rejects:

BLOCKED

NEEDS_CONFIRMATION

UNKNOWN

2️⃣ Confirmation Enforcement

High-risk actions require explicit “yes”:

close app

delete file

shutdown

restart

Runtime handles confirmation lifecycle correctly.

3️⃣ Safety Locks

Prevents:

Dangerous paths (e.g., C:\)

Empty targets

Unsupported commands

Low-confidence unknown inputs

4️⃣ OS Abstraction

Clean architecture:

ExecutionEngine
   ↓
Dispatcher
   ↓
Windows Adapters

Execution layer contains no OS-specific code.

5️⃣ Structured Audit Logging ✅

Implemented ExecutionLogger.

Logs:

timestamp

action

target

success/failure

error_code

Stored in:

execution_logs.json

Audit system complete.

6️⃣ Context + App Stack

Implemented:

close it

go back

switch app

Uses app stack instead of single last_app.

Context updates only after successful execution.

🟡 Runtime Stability (Remaining)

Issue:
Assistant may transcribe its own speech (echo loop).

Needed:

Drop mic audio while speaking

Prevent STT during TTS

Stronger VAD

Minimum speech threshold

This is runtime hardening, not execution failure.

🏁 Phase 3 Completion Status

✔ Execution stable
✔ Confirmation enforced
✔ Safety enforced
✔ App stack implemented
✔ Logging implemented
✔ Audit layer complete
🟡 Runtime echo control pending
🔵 PHASE 4 — Vision Integration

Status: 🟦 Planned

Features

Screen capture

OCR

Object detection

Scene narration

Tech

OpenCV

Tesseract

YOLOv8

🟣 PHASE 5 — Advanced Context Engine

Status: 🟣 Planned

Features

Multi-step memory

Action chaining

Reference resolution graph

Task continuation logic

🟠 PHASE 6 — Gesture Interaction

Status: 🟠 Planned

Features

MediaPipe Hands

Gesture override

Emergency stop

Cursor control

🔴 PHASE 7 — Emotion Awareness

Status: 🔴 Planned

Features

Face emotion detection

Voice stress analysis

Adaptive response tone

Confirmation sensitivity adjustment

🟡 PHASE 8 — Multimodal Fusion Core

Status: 🟡 Critical Future Phase

Goal

Resolve conflicts between:

Voice

Gesture

Vision

Emotion

Guarantee

Exactly ONE safe action will execute.

🟡 PHASE 9 — Adaptive Learning

Status: 🟡 Planned

Features

User preference modeling

Personalized shortcuts

Confirmation tolerance adaptation

Usage pattern learning

🟡 PHASE 10 — UI & Accessibility Profiles

Status: 🟡 Planned

Features

Voice-only mode

Gesture-only mode

Visual feedback dashboard

High-contrast UI

Slow-response mode

Low-motor configuration

🌍 Real-World Impact

Designed for:

Individuals with limited motor control

Hands-free computing environments

Accessibility-focused systems

Safety-sensitive automation

The system prioritizes:

Safety over speed

Determinism over randomness

Confirmation over blind execution

🏁 Current Status Summary
Phase	Status
Phase 1 — Core Engine	✅ Complete
Phase 2 — Voice Runtime	✅ Complete
Phase 3 — Execution Engine	🚧 In Progress
Phase 4 — Vision	🟦 Planned
Phase 5 — Advanced Context	🟣 Planned
Phase 6 — Gesture	🟠 Planned
Phase 7 — Emotion	🔴 Planned
Phase 8 — Multimodal Fusion	🟡 Critical
Phase 9 — Adaptive Learning	🟡 Planned
Phase 10 — UI & Accessibility	🟡 Planned