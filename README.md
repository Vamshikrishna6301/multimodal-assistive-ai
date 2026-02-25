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
│   │
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
│   ├── executor.py
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
│   ├── stt.py
│   ├── tts.py
│   ├── vad.py
│   ├── voice_loop.py
│   └── wakeword.py
│
├── tests/
│   ├── __pycache__/
│   ├── test_execution_vision.py
│   ├── test_router_vision.py
│   ├── test_vision_parser.py
│   ├── test_context.py
│   ├── test_execution_hardening_manual.py
│   ├── test_executor.py
│   ├── test_knowledge.py
│   ├── test_llm_direct.py
│   ├── test_output.py
│   ├── test_parser.py
│   ├── test_phase2_pipeline.py
│   ├── test_response.py
│   ├── test_router.py
│   ├── test_safety.py
│   ├── test_utility.py
│   ├── tests_execution.py
│   └── tests_phase2.py
│
├── .gitignore
│
├── main.py
├── config.py
├── requirements.txt
├── README.md
│
├── demo_full_pipeline.py
├── demo_phase2.py
├── run_phase2_voice.py
│
├── check_active_window.py
├── manual_vision_test.py
├── direct_record_test.py
├── mic_test.py
├── raw_stt_stream_test.py
├── raw_stt_test.py
│
├── intent_parser_reference.py
├── INTENT_PATTERNS_ANALYSIS.json
│
├── execution_logs.json
│
├── test_results.txt
├── test_results_clean.txt
│
└── yolov8n.pt


🟢 PHASE 1 — Core Intent & Safety Engine
Status: ✅ Production Ready
Mission

Build a deterministic, risk-aware decision engine that safely interprets user intent.

Implemented

Structured Intent modeling (confidence, risk level, confirmation flags)

Natural language parsing with rule-based + contextual handling

Context memory (reference resolution: “close it”)

Mode-based interaction control

Safety engine with risk escalation

Confirmation enforcement for high-risk actions

Latency tracking

Deterministic approval flow

Unknown input blocking

Stability

Fully tested

No blocking loops

Fully integrated with voice + vision

🟢 PHASE 2 — Real-Time Voice Runtime
Status: ✅ GPU Optimized | Stable
Mission

Enable fully hands-free interaction via real-time speech.

Technologies

Faster-Whisper (CUDA 12.1)

PyTorch GPU

WebRTC VAD

SoundDevice

Threaded architecture

Non-blocking TTS (PowerShell-based)

Implemented Capabilities

16kHz microphone streaming

Silence-based segmentation

Noise filtering

Speech interruption (“stop”)

Confirmation handling

Runtime state tracking

Clean thread shutdown

Stability

GPU dedicated to Whisper

No speech lag

No thread deadlocks

Clean exit behavior

🟡 PHASE 3 — Execution & Knowledge
Status: ✅ Stable | Production-Functional
Mission

Safely connect approved intents to real-world actions.

3.1 Execution Engine

Windows app control

File operations

Browser search

System control

Safe shutdown / restart

Structured execution logging

Confirmation enforcement

3.2 Utility Engine

Mathematical calculations

System time queries

Lightweight deterministic logic

3.3 Hybrid Knowledge Engine

Wikipedia API for factual queries

TinyLlama (Ollama) for reasoning

Clean summarization (max 2 sentences)

Prompt hardening

No conversational filler

🟢 PHASE 4 — Vision Integration
Status:

🟢 Core Functional
🟢 Runtime Stable
🟡 Intelligence-Level Improvements Pending
🔵 Production Hardening In Progress

🎯 Mission of Phase 4

Transform the assistant from:

Voice-driven OS controller

Into:

Multimodal perceptual assistant capable of understanding and narrating the visual world.

Phase 4 enables environmental awareness.

🏗 WHAT HAS ACTUALLY BEEN ENGINEERED
1️⃣ Screen Vision
File:

execution/vision/screen_capture.py

Capabilities

Full screen capture

Windows-compatible

Integrated into OCR pipeline

Non-blocking execution

2️⃣ OCR Text Reading
File:

execution/vision/ocr_engine.py

Capabilities

Text extraction via Tesseract

Image preprocessing (grayscale, threshold)

Noise cleanup

Speech-friendly formatting

Handles empty results safely

Supported Commands

“read what is on my screen”

“what is on my screen”

3️⃣ Live Camera Object Detection
File:

execution/vision/camera_detector.py

Implemented Features

YOLOv8 inference

CPU-based detection (GPU preserved for Whisper)

Frame skipping (performance tuning)

Confidence filtering (>= 0.5)

Bounding box drawing

Non-blocking daemon thread loop

Stable speech emission (2s interval)

Clean STOP_CAMERA intent

Exit-safe shutdown

Terminal + voice narration

Concurrent voice + vision execution

🧠 Critical Architectural Decision
GPU Resource Isolation Strategy

Device: RTX 2050 (4GB VRAM)

Component	Device
Whisper STT	GPU
YOLO	CPU
OCR	CPU
LLM	CPU
Why?

If YOLO used GPU:

cuDNN conflicts

CUDA memory contention

Audio lag

Runtime instability

Current Result:

Smooth speech

Stable vision

No CUDA crashes

No cuDNN symbol errors

This is production-grade resource isolation.

🔧 Runtime Hardening Completed in Phase 4
✅ Fixed Blocking Camera Loop

Camera moved to daemon thread

STOP_CAMERA intent implemented

Exit safely shuts down all threads

✅ Fixed cuDNN Symbol Error

Forced YOLO to CPU

✅ Fixed NumPy 2.x Crash

Pinned numpy < 2

Ensured Ultralytics compatibility

✅ Fixed OpenMP Duplicate Runtime Crash

Cleaned dependency conflicts

✅ Detection Stability Improvements

Frame skip = 3

Confidence threshold tuned

Speech stabilization interval

Removed over-aggressive temporal locking

🚀 CURRENT CAPABILITIES (Phase 4)

The system can:

✔ Detect objects in real-time
✔ Narrate scene objects
✔ Read screen text
✔ Accept commands during camera mode
✔ Stop camera safely
✔ Exit safely
✔ Maintain concurrent voice + vision

This is a stable multimodal runtime.

🟡 WHAT IS NOT YET PRODUCTION-LEVEL

Currently:

Object detection is implemented.

But production assistive AI requires:

Understanding, tracking, and contextual awareness.

🔴 PHASE 4 MUST EVOLVE INTO

To reach production-grade intelligence, Phase 4 must add:

1️⃣ Object Tracking

Current:
YOLO detects each frame independently.

Missing:

Persistent object identity

Entry/exit detection

Motion tracking

Upgrade:
Add ByteTrack or DeepSORT.

Enables:

“A person entered the room.”

“The phone disappeared.”

Stable bounding boxes

2️⃣ Scene Understanding

Current:
“I see 1 person, 1 phone.”

Production:
“A person is holding a phone.”
“There is a laptop on the table.”

Requires:

Spatial reasoning

Bounding box relationship logic

Lightweight Vision-Language Model (optional)

3️⃣ Smart Object Filtering

Add priority whitelist:

person

chair

door

phone

vehicle

obstacles

Reduce irrelevant detections (fork, tie, toothbrush).

4️⃣ Spatial Awareness

Add:

Left/center/right zone detection

Distance estimation

Object proximity awareness

Enables:
“Person on your left.”
“Phone is in the center.”

5️⃣ Event Detection

Add scene memory:

Object appeared

Object disappeared

Sudden movement

Fall detection

6️⃣ Multimodal Fusion

Currently:
Voice and vision are parallel.

Future:
Voice queries vision.

Example:
User: “Where is my phone?”
System:

Searches frame

Determines position

Responds with spatial guidance

7️⃣ Environmental Modes

Add:

Passive narration

Alert mode

Safety mode

Safety mode:

Fall detection

Fire/smoke detection

Obstacle alerts

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