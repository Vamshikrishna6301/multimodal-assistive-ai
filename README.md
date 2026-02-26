🌍 Project Vision

A safety-first multimodal assistive AI platform designed to empower individuals with physical and motor disabilities by enabling:

🎤 Hands-free system control

🧠 Context-aware decision making

🔒 Risk-controlled execution

🤝 Multimodal interaction (Voice → Gesture → Vision → Emotion)

⚙ Deterministic automation with confirmation safeguards

This system bridges the gap between human intent and digital control in real-world environments.



Voice
↓
Intent Parser
↓
Context Memory
↓
Safety Engine
↓
Fusion Engine
↓
Decision Router
↓
Execution Engine
↓
(UIA Service / OS Adapters / Utility / Knowledge)
↓
User Feedback

📂 Complete Project Structure
KRISHNA/
│
├── __pycache__/
├── .cache/
│
├── core/                              # Phase 1 — Intent & Safety Core
│   ├── __pycache__/
│   ├── __init__.py
│   ├── context_memory.py
│   ├── fusion_engine.py
│   ├── intent_parser.py
│   ├── intent_schema.py
│   ├── mode_manager.py
│   ├── neural_intent_classifier.py
│   ├── response_model.py
│   ├── safety_engine.py
│   └── safety_rules.py
│
├── data/
│
├── execution/                         # Phase 3 — Execution Layer
│   ├── __pycache__/
│   │
│   ├── adapters/                      # OS abstraction layer
│   │   ├── __pycache__/
│   │   ├── windows_app.py
│   │   ├── windows_browser.py
│   │   ├── windows_file.py
│   │   ├── windows_keyboard.py
│   │   └── windows_system.py
│   │
│   ├── uia_service/                   # 🔥 NEW — External UI Automation Service
│   │   ├── __pycache__/
│   │   ├── uia_client.py              # Socket client (used by ExecutionEngine)
│   │   └── uia_server.py              # Standalone UIA socket server
│   │
│   ├── vision/                        # Phase 4 — Vision Integration
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── camera_detector.py
│   │   ├── event_engine.py
│   │   ├── ocr_engine.py
│   │   ├── scene_graph_engine.py
│   │   ├── scene_memory.py
│   │   ├── screen_capture.py
│   │   ├── screen_monitoring_engine.py
│   │   ├── stabilization_buffer.py
│   │   ├── tracking_engine.py
│   │   ├── vision_executor.py
│   │   ├── vision_mode_controller.py
│   │   └── vision_query_engine.py
│   │
│   ├── dispatcher.py                  # Routes execution to adapters
│   ├── execution_logger.py            # Execution audit layer (partial)
│   ├── executor.py                    # 🔥 Main ExecutionEngine
│   ├── file_ops.py
│   └── keyboard_mouse.py
│
├── infrastructure/                    # Production runtime infrastructure
│   ├── __pycache__/
│   ├── __init__.py
│   ├── cache.py
│   ├── config_manager.py
│   ├── error_handling.py
│   ├── health_monitor.py
│   ├── logger.py
│   ├── persistence.py
│   ├── production_logger.py
│   ├── system_monitor.py
│   └── validation.py
│
├── knowledge/                         # Phase 3.3 — Knowledge Layer
│   ├── __pycache__/
│   ├── knowledge_engine.py            # Wikipedia
│   └── llm_engine.py                  # Local LLM (TinyLlama / Ollama)
│
├── logs/
│
├── models/
│
├── phase4_ai_intelligence/
│
├── router/                            # Phase 3 — Decision Router
│   ├── __pycache__/
│   └── decision_router.py
│
├── tests/
│
├── utility/                           # Phase 3.2 — Utility Engine
│   ├── __pycache__/
│   └── utility_engine.py
│
├── voice/                             # Phase 2 — Voice Runtime
│   ├── __pycache__/
│   ├── assistant_runtime.py
│   ├── mic_stream.py
│   ├── stt.py
│   ├── tts.py
│   ├── vad.py
│   ├── voice_loop.py
│   └── wakeword.py
│
├── .gitignore
├── config.py
├── main.py                            # 🔥 Main system entrypoint
│
├── debug_tools/                       # (Recommended grouping)
│   ├── camera_index_test.py
│   ├── check_active_window.py
│   ├── debug_startup.py
│   ├── debug_startup2.py
│   └── direct_record_test.py
│
├── demos/
│   ├── demo_phase2.py
│   ├── demo_full_pipeline.py
│   ├── demo_phase4_camera_visual.py
│   ├── demo_phase4_live_corrected.py
│   ├── demo_phase4_text_visual.py
│   └── demo_phase4_vision.py
│
└── README.md

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

❌ Close Notepad Not Working

Cause: WindowsSystemAdapter.handle() incomplete.

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




🆕 Major Architecture Upgrade (Phase 3 Final Form)

During runtime stabilization and UI integration, the architecture was significantly upgraded.

🔥 External UIA Service (New)

UI automation was extracted into a separate socket-based service:

Assistant → UIAClient (socket) → UIA Server → pywinauto
Why This Was Done

Previously:

UIA ran inside main assistant thread

Thread locks caused freezes

UI traversal blocked voice loop

Deadlocks occurred

Now:

UIA runs as isolated service

No cross-thread COM conflicts

No UI freeze blocking voice

Clean separation of concerns

🖱 Semantic UI Control (Now Working)

The assistant now supports:

✅ Screen Reading

"What is on my screen?"

Returns:

Active window name

Interactive elements (indexed)

Element type + name

Works across:

Notepad

File Explorer

VS Code

Chrome

Windows Settings

Any UIA-compatible Windows app

✅ Click by Index

"Click 5"
"Click number 3"

Works reliably.

✅ Click by Name (New)

"Click edit"
"Click file"
"Click view"
"Click bold"

Supported via:

action = CLICK_NAME
parameters = {"name": "edit"}

Fixed routing bug where CLICK_NAME was not reaching ExecutionEngine.

🧠 Router Architecture Fix (Critical Fix)

Previously:

if action in EXECUTION_ACTIONS:

This caused:

CLICK_NAME not routed

Unsupported action errors

Now:

All non-utility / non-knowledge actions
→ go directly to ExecutionEngine

This prevents future routing bugs.

🔌 UIA Communication Protocol (Final Form)
Server

Raw TCP socket

JSON payload

No HTTP

No Flask

No requests library

Client

Raw socket

Sends JSON

Receives JSON

Decodes safely

Fix resolved:

BadStatusLine
Connection aborted
Unsupported action type
🎤 Runtime Stability Issues (Important)

The assistant previously appeared to "freeze" after one command.

🔎 Root Cause

Not execution bug.

Acoustic feedback loop:

Assistant speaks

Microphone captures speaker audio

VAD detects as speech

STT transcribes assistant’s own voice

Fake intents generated

This created illusion of freeze.

🛠 Required Runtime Hardening (Still Recommended)

Before full production:

Drop mic frames while speaking

Increase VAD aggressiveness (Level 3)

Enforce minimum speech duration

Prevent STT while TTS active

Add echo cancellation (future improvement)

🟢 Phase 3 — Execution Engine (Current State)
✅ Now Working

UIA read screen

Click by index

Click by name

OS abstraction layer

Confirmation enforcement

Risk validation

Decision validation

Router stability

External UIA isolation

⚠ Still Needs Improvement

Execution logging not fully implemented

Some Windows adapters incomplete

Close Notepad occasionally inconsistent

No persistent action audit log

No retry policy for UI failures

No timeout protection on UIA service

🟢 Phase 4 — Vision Integration

Status: ✅ Stable

Includes:

Screen OCR

YOLOv8 object detection

Scene graph reasoning

Detection stabilization

Mode-based behavior

Camera tracking

Screen monitoring

Now fully integrated with voice runtime.

🧪 Updated Testing Status
UIA Tests
Command	Status
Read screen	✅
Click by index	✅
Click by name	✅
Cross-application support	✅
Runtime Stability
Scenario	Status
Back-to-back commands	⚠ Needs improvement
Echo suppression	⚠ Partial
Interrupt while speaking	✅
Silence handling	✅
Voice
↓
Intent Parser
↓
Context Memory
↓
Safety Engine
↓
Fusion Engine
↓
Decision Router
↓
Execution Engine
↓
(UIA Service / OS Adapters / Utility / Knowledge)
↓
User Feedback