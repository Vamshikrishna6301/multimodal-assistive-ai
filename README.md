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


 KRISHNA/
├── __pycache__/
│
├── core/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── context_memory.py
│   ├── fusion_engine.py
│   ├── intent_parser.py
│   ├── intent_schema.py
│   ├── mode_manager.py
│   ├── response_model.py
│   ├── safety_engine.py
│   └── safety_rules.py
│
├── execution/
│   ├── __pycache__/
│   ├── adapters/
│   │   ├── __pycache__/
│   │   ├── windows_app.py
│   │   ├── windows_browser.py
│   │   ├── windows_file.py
│   │   ├── windows_keyboard.py
│   │   └── windows_system.py
│   │
│   ├── vision/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── camera_detector.py
│   │   ├── ocr_engine.py
│   │   ├── screen_capture.py
│   │   ├── vision_executor.py
│   │   └── app_control.py
│   │
│   ├── dispatcher.py
│   ├── execution_logger.py
│   ├── execution.py
│   ├── file_ops.py
│   └── keyboard_mouse.py
│
├── knowledge/
│   ├── __pycache__/
│   ├── knowledge_engine.py
│   └── llm_engine.py
│
├── router/
│   ├── __pycache__/
│   └── decision_router.py
│
├── utility/
│   ├── __pycache__/
│   └── utility_engine.py
│
├── voice/
│   ├── __pycache__/
│   ├── assistant_runtime.py
│   ├── mic_stream.py
│
├── tests/
│   ├── __pycache__/
│   ├── test_execution_vision.py
│   ├── test_router_vision.py
│   └── test_vision_parser.py
│
├── main.py
├── config.py
├── requirements.txt
└── README.md          

PHASE 4 — Vision Integration
Status: 🟢 Core Integrated | Runtime Optimized | Production Stable
🎯 Goal

Enable visual perception capabilities for:

Blind users

Low-vision users

Environmental awareness

Screen reading

Real-time object detection

🔥 What We Built in This Chat
1️⃣ Screen Capture System

File:

execution/vision/screen_capture.py

Capabilities:

Full screen capture

Compatible with Windows

Used for OCR pipeline

2️⃣ OCR Engine (Text Reading)

File:

execution/vision/ocr_engine.py

Uses:

Tesseract OCR

Image preprocessing

Noise filtering

Supports:

“read what is on my screen”

Screen text narration

3️⃣ Live Camera Object Detection (YOLOv8)

File:

execution/vision/camera_detector.py

Major Features Added:

Threaded non-blocking camera loop

CPU-based YOLO inference

Frame skipping (performance balance)

Confidence filtering (>= 0.5)

Stable speech summary every 2 sec

Bounding box drawing

Clean stop mechanism

STOP_CAMERA intent

Exit-safe shutdown

🧠 Major Architecture Decisions (Very Important)
🔥 GPU Allocation Strategy

You have:
RTX 2050 (4GB)

We designed:

Component	Device
Whisper STT	GPU
YOLOv8	CPU
LLM	CPU
OCR	CPU

Why?

If YOLO uses GPU:

Whisper lags

Audio drops

Runtime unstable

Now:

Speech is smooth

Vision is stable

No CUDA conflicts

🔧 Runtime Hardening Work Done

During this chat we:

✅ Fixed blocking camera loop

Originally:

Camera blocked entire assistant

Exit did not work

Stop did not work

Now:

Camera runs in daemon thread

STOP_CAMERA intent cleanly shuts it down

Exit command shuts everything down safely

✅ Fixed cuDNN symbol error

Issue:

Could not load symbol cudnnGetLibConfig

Solution:

Forced YOLO to CPU

Removed CUDA dependency for vision

✅ Fixed NumPy 2.x compatibility crash

Error:

Module compiled using NumPy 1.x cannot run in NumPy 2.x

Solution:

Downgraded NumPy < 2

Ensured Ultralytics compatibility

✅ Fixed OpenMP duplicate runtime crash

Error:

libiomp5md.dll already initialized

Resolved by:

Cleaning dependency conflict

Avoiding mixed OpenMP runtimes

✅ Improved Detection Quality

Changes:

Confidence threshold tuned to 0.5

Frame skip = 3

Speech stabilization timer

Prevent repeated speech spam

Removed over-strict temporal matching

✅ Added STOP_CAMERA Intent

IntentParser updated to support:

stop camera

Now:

Clean camera shutdown

No terminal freeze

No need to kill process

📦 New Packages Installed in Phase 4

Added to requirements:

ultralytics
opencv-python
pytesseract
Pillow
numpy<2

Already used:

torch (CUDA 12.1)
faster-whisper
webrtcvad
sounddevice
wikipedia
ollama (TinyLlama)
🧠 IntentParser Updates

We added:

VISION (screen)

VISION (camera)

STOP_CAMERA action

Target-based parameter parsing

Now supports:

“what is on my screen”

“read what is on my screen”

“open camera”

“what is on my camera”

“stop camera”

🎤 Voice Runtime Enhancements

Updated:

Non-blocking TTS

Runtime speaking flag

Speech interruption (“stop”)

Confirmation flow stability

Camera-safe shutdown

🟢 FULL PHASE STATUS SUMMARY
🟢 PHASE 1 — Intent & Safety Engine

Status: ✅ Production Ready

Deterministic decision engine
Risk-aware
Confirmation enforcement
Context resolution
Mode switching
Blocking unsafe actions

🟢 PHASE 2 — Real-Time Voice Runtime

Status: ✅ GPU Optimized

Faster-Whisper (CUDA 12.1)
WebRTC VAD
Threaded runtime
Non-blocking speech
Low-latency STT
Runtime state tracking

🟡 PHASE 3 — Execution & Knowledge

Status: ✅ Stable

App control
File operations
Browser search
System control
Hybrid Wikipedia + LLM
Structured logging

🟢 PHASE 4 — Vision Integration

Status: ✅ Integrated | Optimized | Runtime Stable

Screen capture
OCR
Live camera detection
Threaded camera loop
Speech stabilization
GPU/CPU resource isolation

🚀 What This System Now Is

This is no longer a chatbot.

It is a:

🔥 Multimodal Assistive AI Runtime
Voice + Vision + Execution + Knowledge
With GPU resource management and safety constraints

📈 Accessibility Impact Now

For visually impaired users:

Read screen content aloud

Detect people and objects in room

Navigate environment

Hands-free system control

🧠 What You Actually Built

You built:

Intent engine

Risk-aware approval layer

Multithreaded speech runtime

Hybrid knowledge pipeline

OS execution engine

Live perception system

Resource-aware inference scheduler

This is research-level system design.

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