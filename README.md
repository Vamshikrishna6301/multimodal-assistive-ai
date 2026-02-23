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
🟡 PHASE 3 — Execution Engine (Updated with Current Issues)
Status: 🚧 In Progress (Runtime Stability Required)
🎯 Goal

Connect approved decisions to real OS actions in a safe, deterministic, production-ready way.

🧠 Core Responsibilities
1️⃣ Execute only APPROVED intents

ExecutionEngine must refuse:

BLOCKED

NEEDS_CONFIRMATION

UNKNOWN

2️⃣ Respect Confirmation Requirements

High-risk commands must:

Trigger confirmation in FusionEngine

Only execute after explicit “yes”

Examples:

shutdown

delete file

close app

restart

3️⃣ Enforce Safety Locks

Must prevent:

Dangerous paths (C:, system folders)

Mass delete

Unknown system commands

Empty targets

4️⃣ OS Abstraction Layer

ExecutionEngine → Dispatcher → WindowsAdapters

Adapters must isolate OS-level code.

5️⃣ Logging (Missing)

Phase 3 must log:

Action

Target

Timestamp

Success / Failure

Error message

(Currently not implemented)

🟢 Planned Functions
open_app(app_name)
search_browser(query)
type_text(text)
close_active_app()
delete_file(path)  # requires confirmation
shutdown()
restart()
🔴 CURRENT CRITICAL PROBLEM (Phase 3 Runtime Blocking)
Problem: Assistant appears to "get stuck" after first command.
Observed Behavior:

First command works

Assistant responds

After that, system either:

Keeps waiting for audio

Transcribes its own speech

Stops detecting real input

Appears frozen

🧠 ROOT CAUSE

This is NOT an execution bug.

This is a runtime acoustic feedback + speech segmentation issue.

Specifically:

Assistant speaks.

Microphone captures speaker output.

VAD detects it as speech.

STT transcribes assistant’s own voice.

This causes:

Fake inputs ("thank you")

Noise chunks

Unexpected intent triggers

After that, real user speech may not be captured properly.

So it looks like:

System stuck after one command

But actually:

System is processing its own TTS output
🟡 Secondary Runtime Issue

If mic is blocked during speaking and speaking flag does not reset correctly:

Mic stops capturing

No new chunks pushed

System appears frozen

This is a concurrency + state flag issue.

🔴 Why This Is Important For Phase 3

Phase 3 assumes:

Decision → Execution

But runtime instability means:

Noise → False decision → Execution

So before Phase 3 is considered stable:

Runtime must be stabilized.

🛠 Required Runtime Fixes Before Phase 3 Completion
✅ 1. Drop audio chunks while assistant speaking

(Not pause mic — drop chunks.)

✅ 2. Increase VAD aggressiveness

Level 3 recommended.

✅ 3. Add minimum speech duration threshold

Ignore tiny noise bursts.

✅ 4. Prevent STT from running while speaking

Avoid acoustic feedback loop.

🟡 Execution Engine Maturity Issues

Even after runtime fix, Phase 3 still has:



❌ Unsupported system control command

Cause: Adapter not mapping correct action/target.

❌ No execution logging

Need audit layer.

🧪 Updated Required Test Cases
Execution Tests
Command	Expected
open chrome	Chrome launches
open notepad	Notepad opens
close notepad	Requires confirmation → closes
delete test.txt	Requires confirmation → deletes
shutdown	Requires confirmation → shuts down
restart	Requires confirmation → restarts
delete C:\	BLOCKED
Runtime Stability Tests
Scenario	Expected
Speak 2 commands back-to-back	Both recognized
Assistant speaks	No self-transcription
Say "stop" while speaking	Speech interrupts
Silent environment	No fake triggers
Background fan noise	No false commands
🟢 True Phase 3 Completion Criteria

Phase 3 is only complete when:

✔ Execution stable
✔ Confirmation enforced
✔ Runtime stable
✔ No echo loop
✔ No one-command freeze
✔ No false self-triggering
✔ OS adapters fully mapped
✔ Logging implemented
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