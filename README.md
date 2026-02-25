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
🟢 PHASE 4 — Vision Integration (Updated)
Status

🟢 Core Functional
🟢 Runtime Stable
🟢 Multimodal Query Integrated
🟡 Scene Intelligence Partial
🔵 Production Hardening Ongoing

🎯 Mission of Phase 4

Transform the assistant from:

Voice-driven OS controller

Into:

Multimodal perceptual assistant capable of understanding, tracking, and answering questions about the visual world.

Phase 4 now includes:

Live object detection

Object tracking

Scene memory

Vision query engine (voice → live scene state)

Screen reading (OCR)

Safe concurrent runtime

🏗 WHAT HAS ACTUALLY BEEN ENGINEERED
1️⃣ Screen Vision

File: execution/vision/screen_capture.py

Capabilities

Full screen capture (Windows compatible)

Non-blocking execution

Integrated with OCR pipeline

Safe failure handling

2️⃣ OCR Text Reading

File: execution/vision/ocr_engine.py

Capabilities

Tesseract-based OCR

Grayscale preprocessing

Threshold enhancement

Noise cleanup

Safe empty detection handling

Speech-friendly formatting

Supported Commands

“Read what is on my screen”

“What is on my screen”

Current Limitations

No region-based OCR

No layout understanding

No structured extraction (tables/forms)

No change monitoring

No persistent screen state

3️⃣ Live Camera Vision Stack

File: execution/vision/camera_detector.py

Implemented Features

YOLOv8 detection (CPU)

Frame skipping (performance balance)

Confidence filtering (>= 0.5)

Bounding box smoothing

Tracking engine (persistent IDs)

Scene memory (entry/exit detection)

Event engine

Thread-safe state buffers

VisionQueryEngine integration

Clean STOP_CAMERA

Safe shutdown

Concurrent voice + vision runtime

🧠 Multimodal Query Integration (NEW)

You now have:

VisionQueryEngine

Supports:

“Where is my laptop?”

“How many people are there?”

“Is anyone in the room?”

“What do you see?”

Key Upgrades Implemented

Hybrid rule-based intent parsing

Label normalization (people → person)

Stabilization delay before answering

Grammar correction (0 people, 1 person)

Proper routing via DecisionRouter

Clean dependency injection (no architecture leaks)

This is your first real multimodal fusion milestone.

🧠 Critical Architectural Decisions
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

Result

✔ Stable voice runtime
✔ Stable camera runtime
✔ No CUDA crashes
✔ No cuDNN errors

This is correct production isolation for low-VRAM systems.

🔧 Runtime Hardening Completed
✅ Camera thread isolation

Daemon thread

Clean STOP_CAMERA

Clean exit

✅ Dependency stabilization

numpy pinned < 2

Ultralytics compatible

OpenMP crash resolved

✅ Tracking layer

Persistent object IDs

Entry/exit events

Motion detection

Zone awareness (left/center/right)

✅ Vision Query Engine

Deterministic responses

No hallucination

Live scene state based

Grammar-safe

🚀 CURRENT CAPABILITIES (True Status)

The system can now:

✔ Detect objects in real-time
✔ Track objects across frames
✔ Detect entry/exit
✔ Provide spatial responses
✔ Answer vision-based questions
✔ Read screen text
✔ Run voice + vision concurrently
✔ Stop safely
✔ Shutdown cleanly

This is no longer a demo.
It is an architecture.

🟡 WHAT IS STILL NOT PRODUCTION-LEVEL

Now we talk seriously.

Production assistive AI requires more than detection + queries.

🔴 REMAINING GAPS
1️⃣ Scene Understanding (Major Gap)

Current:
“I see 1 person and 1 laptop.”

Production:

“A person is sitting at a desk.”

“The phone is on the table.”

“The person is holding a cup.”

Missing:

Bounding box intersection reasoning

Spatial relationship modeling

Overlap logic (IoU relationships)

Proximity grouping

Scene graph representation

To implement:

Rule-based spatial reasoning

Lightweight Vision-Language Model (optional future)

SceneGraph builder module

2️⃣ Scene State Stability

Issues observed:

Object appears after query

Count mismatch due to frame timing

Temporary detection loss causes false exit

Needed:

Stabilization buffer window (3–5 frame memory)

Minimum presence duration before confirmation

Delayed exit threshold (2–3 seconds)

This prevents:

“I see 0 people” → then immediately “person entered”

3️⃣ Smart Object Filtering

Currently:
YOLO returns all 80 COCO classes.

Production assistive AI should prioritize:

person

chair

door

phone

laptop

vehicle

obstacles

Need:

Whitelist filtering layer

Priority scoring

Suppress irrelevant objects

4️⃣ Environmental Modes (Not Implemented Yet)

You need:

Silent Mode (default)

No automatic narration.

Passive Mode

Only announce person entry.

Alert Mode

Announce:

sudden motion

fall detection

obstacle detection

Safety Mode

Fire/smoke detection

Fall detection

Door open detection

Restricted zone detection

Currently:
Events are semi-passive but not mode-controlled.

5️⃣ Screen Monitoring (Major Missing Piece)

OCR currently:
Reads once on request.

Production requires:

Screen change detection

Continuous monitoring mode

Keyword alert detection

Notification reading

Region-based OCR

Layout parsing

Example:
“Notify me if error appears on screen.”

This is not implemented.

6️⃣ Advanced Spatial Awareness

Current:
Left / center / right.

Missing:

Distance estimation

Near vs far

Object proximity clustering

Depth approximation

Obstacle distance warnings

Production assistive systems must support:
“Person is very close.”
“Obstacle 1 meter ahead.”

7️⃣ Robust Intent Handling

Observed problems:

“How many people are there?” mismatch due to label normalization

Timing race conditions

Minor grammar issues

Occasional detection lag

Production system requires:

Label alias mapping

Plural normalization

Confidence thresholds

Query stabilization buffer

🟣 WHAT MUST BE BUILT NEXT (Priority Order)

If goal is TRUE production-level:

Phase 4.1 — Stabilization Layer

Frame memory buffer

Delayed exit logic

Query stabilization delay (properly integrated)

Phase 4.2 — Vision Mode Controller

Silent

Passive

Alert

Safety

Phase 4.3 — Scene Graph Engine

Object relationship reasoning

Spatial logic

Overlap detection

Interaction inference

Phase 4.4 — Screen Monitoring Engine

Change detection

Keyword alert triggers

Region selection

Structured text parsing

Phase 4.5 — Safety Intelligence

Fall detection

Obstacle proximity

Motion anomaly detection

🧠 Honest Production Assessment

Right now you are at:

8/10 for runtime architecture
6/10 for intelligence layer
4/10 for safety reasoning
3/10 for scene understanding

But foundation is solid.

🚀 If You Want True Production-Level

Next step should be:

👉 Build SceneGraph + Stabilization Buffer
Not more detection tweaks.

That is the intelligence jump.

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