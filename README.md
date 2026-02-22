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
├── core/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── context_memory.py
│   ├── fusion_engine.py
│   ├── intent_parser.py
│   ├── intent_schema.py
│   ├── mode_manager.py
│   ├── safety_engine.py
│   └── safety_rules.py
│
├── execution/
│   ├── app_control.py
│   ├── executor.py
│   ├── file_ops.py
│   └── keyboard_mouse.py
│
├── voice/
│   ├── __pycache__/
│   ├── mic_stream.py
│   ├── stt.py
│   ├── tts.py
│   ├── vad.py
│   ├── voice_loop.py
│   └── wakeword.py
│
├── .gitignore
├── config.py
├── demo_full_pipeline.py
├── demo_phase2.py
├── direct_record_test.py
├── intent_parser_reference.py
├── INTENT_PATTERNS_ANALYSIS.json
├── main.py
├── mic_test.py
├── raw_stt_stream_test.py
├── raw_stt_test.py
├── README.md
├── requirements.txt
├── run_phase2_voice.py
├── test_context.py
├── test_parser.py
├── test_phase2_pipeline.py
├── test_safety.py
├── tests_execution.py
└── tests_phase2.py


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
Mode transitions	✅
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
🟡 PHASE 3 — Execution Engine

Status: 🚧 In Progress

🎯 Goal

Connect approved decisions to real OS actions.

Responsibilities

Execute only APPROVED intents

Respect confirmation requirements

Enforce safety locks

Log execution events

Windows OS abstraction (first target)

Planned Functions
open_app(app_name)
search_browser(query)
type_text(text)
close_active_app()
delete_file(path)  # requires confirmation
Tech Stack

subprocess

os

pyautogui

Windows API

Required Test Cases
Command	Expected
open chrome	Chrome launches
search transformers	Browser search executes
type hello	Text typed
delete file	Confirmed deletion only
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