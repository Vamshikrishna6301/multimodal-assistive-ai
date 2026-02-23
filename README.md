Project Vision

This project is an AI-powered multimodal personal assistant tailored for differently-abled individuals, including:

Visually impaired users

Motor-disabled users

Speech-impaired users

Users with limited mobility or coordination

Users requiring adaptive interaction models

The system enables natural, intuitive, and safe interaction with both digital and physical environments using:

🎤 Voice input and output

✋ Gesture recognition

👁 Vision-based perception

😊 Emotion awareness

🧠 Context-aware reasoning

🎯 Core Objective

To bridge the gap between human intent and machine execution by building a deterministic, safety-aware, multimodal assistive intelligence system that:

Reduces dependency on traditional input devices (keyboard, mouse)

Provides accessible computing interfaces

Ensures safe automation through confirmation safeguards

Maintains contextual awareness across interactions

Supports adaptive interaction based on user capability

🔐 Foundational Design Principles

The system is built on the following non-negotiable guarantees:

Deterministic decision logic

Explicit confirmation for high-risk actions

Single-action safe execution model

Context retention for multi-step interaction

Accessibility-first design

Safety over speed

Structured audit logging for transparency

🏗 High-Level System Architecture
Voice / Gesture / Vision / Emotion Inputs
                  ↓
           Intent Parsing Layer
                  ↓
           Context Memory
                  ↓
           Safety Evaluation
                  ↓
           Fusion Engine
                  ↓
           Decision Routing
                  ↓
           Execution Engine
                  ↓
           Adaptive User Feedback



           project_root/
│
├── core/                          # Phase 1 — Intent & Safety Core
│   ├── context_memory.py
│   ├── fusion_engine.py
│   ├── intent_parser.py
│   ├── intent_schema.py
│   ├── mode_manager.py
│   ├── safety_engine.py
│   ├── safety_rules.py
│   └── response_model.py
│
├── router/                        # Phase 3 — Decision Routing
│   └── decision_router.py
│
├── execution/                     # Phase 3.1 — Execution Engine
│   ├── executor.py
│   ├── dispatcher.py
│   ├── execution_logger.py
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
│   ├── knowledge_engine.py
│   └── llm_engine.py
│
├── voice/                         # Phase 2 — Real-Time Runtime
│   ├── assistant_runtime.py
│   ├── mic_stream.py
│   ├── vad.py
│   ├── stt.py
│   ├── tts.py
│   └── voice_loop.py
│
├── tests/
│   ├── test_context.py
│   ├── test_parser.py
│   ├── test_safety.py
│   ├── test_execution.py
│   └── test_voice_pipeline.py
│
├── demos/
│   ├── demo_phase2.py
│   └── demo_full_pipeline.py
│
├── config.py
├── main.py
├── requirements.txt
└── README.md

🟢 PHASE 1 — Core Intent & Safety Engine

Status: ✅ Complete

Goal

Create a deterministic, risk-aware decision engine capable of safely interpreting user intent.

Key Features

Structured Intent modeling (confidence, risk level, confirmation flags)

Flexible natural language parsing

Context memory for reference resolution

Mode-based interaction control

Hard blocking for unsafe operations

Latency tracking

Deterministic approval flow

Technologies Used

Python 3.x

Dataclasses

Threading

Regular Expressions

Structured JSON logging

Test Coverage

Command recognition accuracy

Risk escalation handling

Confirmation enforcement

Context resolution (“close it”)

Mode switching validation

Unknown input blocking

🎤 PHASE 2 — Real-Time Voice Runtime

Status: ✅ Complete

Goal

Enable hands-free operation through robust, real-time speech processing.

Technologies

Faster-Whisper (GPU STT)

PyTorch CUDA

WebRTC VAD

SoundDevice

NumPy

Offline TTS (PowerShell / pyttsx3)

Multi-threaded runtime architecture

Capabilities

Real-time microphone streaming (16kHz)

Silence-based segmentation

Noise filtering

Echo mitigation

Non-blocking TTS

Confirmation voice loop

Runtime state management

Accessibility Impact

Enables blind and low-mobility users to operate systems without physical input devices.

Allows hands-free navigation and application control.

🟡 PHASE 3 — Execution & Knowledge Integration

Status: 🟡 Execution Complete | Runtime Hardening Ongoing

Goal

Safely connect approved intents to real-world system actions.

3.1 Execution Engine
Features

Approved-only execution

Confirmation-required enforcement

OS abstraction via adapter layer

App stack tracking

Safe shutdown & restart controls

Structured execution logging

Logging System

Each action logs:

Timestamp

Action

Target

Risk level

Confirmation state

Success / Failure

Error code

Spoken response

Audit-ready.

3.2 Utility Engine

Handles:

Mathematical calculations

System time queries

Deterministic lightweight queries

3.3 Hybrid Knowledge Engine

Combines:

Wikipedia API (fast factual queries)

Local LLM (TinyLlama via Ollama) for reasoning

Features

Clean output formatting

Disambiguation filtering

Factual summarization (max 2 sentences)

LLM prompt hardening

No conversational filler

Offline capability (LLM)

🔵 PHASE 4 — Vision Integration (Planned)

Status: 🟦 Planned

Objective

Enable visual perception for blind and visually impaired users.

Planned Capabilities

Screen capture

OCR text extraction

Object detection (real-world camera)

Scene narration

Environmental awareness

Technologies

OpenCV

Tesseract OCR

YOLOv8

NumPy

Accessibility Impact

Describes surroundings

Reads text from screen or environment

Assists in navigation

🟣 PHASE 5 — Advanced Context Engine (Planned)

Multi-step task chaining

Task continuation memory

Reference resolution graph

Intelligent action linking

🟠 PHASE 6 — Gesture Interaction (Planned)

MediaPipe Hands

Gesture-to-command mapping

Cursor control

Emergency stop gesture

Override capability

Accessibility impact:
Enables interaction for users unable to speak clearly.

🔴 PHASE 7 — Emotion Awareness (Planned)

Facial emotion detection

Voice stress analysis

Adaptive response tone

Confirmation sensitivity adjustment

Accessibility impact:
Improves interaction comfort and reduces cognitive load.

🟡 PHASE 8 — Multimodal Fusion Core (Critical Phase)

Goal:

Resolve conflicts between:

Voice

Gesture

Vision

Emotion

Guarantee:

Exactly one safe action executes at a time.

Implements modality prioritization and confidence arbitration.

🟡 PHASE 9 — Adaptive Learning

Personalized shortcuts

Usage pattern modeling

Confirmation tolerance adaptation

Preference memory

🟡 PHASE 10 — Accessibility Profiles & UI Layer

Voice-only mode

Gesture-only mode

High-contrast dashboard

Slow-response mode

Low-motor configuration

Feedback customization

🌍 Real-World Applications

Assistive computing for differently-abled individuals

Hospital bedside interaction systems

Smart home accessibility

Hands-free industrial control

Safety-critical environments

Accessibility research platforms

🏁 Current Development Status
Phase	Status
Phase 1 — Core Engine	✅ Complete
Phase 2 — Voice Runtime	✅ Complete
Phase 3 — Execution & Knowledge	🟡 Stable
Phase 4 — Vision	🟦 Planned
Phase 5 — Advanced Context	🟣 Planned
Phase 6 — Gesture	🟠 Planned
Phase 7 — Emotion	🔴 Planned
Phase 8 — Multimodal Fusion	🟡 Critical
Phase 9 — Adaptive Learning	🟡 Planned
Phase 10 — Accessibility UI	🟡 Planned