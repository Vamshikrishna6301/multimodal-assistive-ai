# 🧠 Multimodal Assistive AI Personal Assistant
### Voice • Vision • Gesture • Context • Safety • Adaptation

> A **voice-first, decision-driven multimodal personal assistant** designed especially for differently-abled users  
> Built phase-by-phase with **low latency, safety, explainability, and modularity** as core principles.

This is **NOT a chatbot**.  
This is an **assistive AI system** that safely controls a computer and environment.

---

## 📌 CORE DESIGN PHILOSOPHY

Multiple Inputs → One Decision Engine → One Safe Action


- Inputs: Voice, Vision, Gesture, Emotion, Context
- Intelligence: Rule-based + ML-assisted (hybrid AI)
- Safety > Intelligence
- LLMs are helpers, never controllers

---

## 📁 COMPLETE FILE STRUCTURE (CURRENT + FUTURE)

KRISHNA/
│
├── voice/ # Phase 1
│ ├── init.py
│ ├── mic_stream.py # Microphone streaming
│ ├── vad.py # Voice Activity Detection
│ ├── stt.py # Speech-to-Text (Whisper)
│ ├── tts.py # Text-to-Speech (edge-tts)
│ ├── wakeword.py # Fuzzy wake word detection
│ └── voice_loop.py # Full duplex voice loop
│
├── core/ # Phase 2, 5, 8
│ ├── init.py
│ ├── intent_schema.py # Intent dataclasses
│ ├── intent_parser.py # Rule-based intent parsing
│ ├── mode_manager.py # COMMAND / DICTATION / QUESTION
│ ├── safety_rules.py # Confirmation & blocking
│ ├── context_memory.py # Session memory
│ ├── intent_buffer.py # Multimodal buffering
│ ├── priority_rules.py # Conflict resolution
│ └── fusion_engine.py # Phase 8 core
│
├── execution/ # Phase 3
│ ├── app_control.py
│ ├── keyboard_mouse.py
│ └── file_ops.py
│
├── vision/ # Phase 4
│ ├── screen_capture.py
│ ├── camera_capture.py
│ ├── ocr_reader.py
│ └── object_detection.py
│
├── gesture/ # Phase 6
│ ├── hand_tracker.py
│ └── gesture_rules.py
│
├── emotion/ # Phase 7
│ ├── face_emotion.py
│ └── voice_stress.py
│
├── learning/ # Phase 9
│ └── adaptive_rules.py
│
├── ui/ # Phase 10
│ └── dashboard.py
│
├── config.py
├── main.py
├── requirements.txt
└── README.md


---

## 🟢 PHASE 1 — VOICE I/O FOUNDATION  
**Status: ✅ COMPLETED (CPU stable)**

### Goal
Build a **real-time, low-latency, full-duplex voice pipeline**

### Features
- Microphone streaming
- Voice Activity Detection (VAD)
- Speech-to-Text (Whisper)
- Text-to-Speech (Windows-safe)
- Wake-word based activation
- Noise tolerance
- Continuous listening

### Functions / Modules
- `MicrophoneStream.read()`
- `VAD.is_speech()`
- `STT.transcribe()`
- `TTS.speak()`
- `is_wake_word()`
- `VoiceLoop.run()`

### Tech Stack
- `sounddevice`
- `webrtcvad`
- `faster-whisper` (CPU)
- `edge-tts`
- `numpy`

### Test Cases
| Test | Expected |
|----|----|
Silence | No output |
Noise | Ignored |
Wake word | Voice reply |
Repeated wake word | Responds |
Long run | No crash |

---

## 🟡 PHASE 2 — INTENT & MODE ENGINE  
**Status: ⏳ NEXT**

### Goal
Understand **what kind of input** the user gave

### Features
- Intent schema (dataclasses)
- Rule-based intent parsing
- Modes:
  - COMMAND
  - DICTATION
  - QUESTION
  - DISABLED
- Safety confirmations

### Functions / Modules
- `Intent(type, action, target, params)`
- `parse_intent(text)`
- `ModeManager.set_mode()`
- `SafetyRules.requires_confirmation()`

### Tech Stack
- Python `dataclasses`
- Regex / keyword rules
- Finite state machine

### Test Cases
| Input | Result |
|----|----|
Open Chrome | COMMAND |
Type hello | DICTATION |
Delete all files | Confirmation |
Disable assistant | Ignored |

---

## 🟡 PHASE 3 — TASK EXECUTION ENGINE  
**Status: ⏳ PLANNED**

### Goal
Execute **real OS actions** safely

### Features
- Open / close applications
- Browser search & playback
- Keyboard automation
- Mouse automation
- File operations

### Functions / Modules
- `open_app()`
- `search_browser()`
- `type_text()`
- `scroll()`
- `close_active_app()`

### Tech Stack
- `pyautogui`
- `subprocess`
- `os`, `platform`

### Test Cases
| Command | Result |
|----|----|
Open Chrome | Browser opens |
Search today score | Results shown |
Play YouTube video | Video plays |
Close it | App closes |

---

## 🟡 PHASE 4 — VISION → VOICE  
**Status: ⏳ PLANNED**

### Goal
Describe **screen & surroundings** via voice

### Features
- Screen capture
- Camera capture
- OCR reading
- Object detection
- Spoken narration

### Functions / Modules
- `capture_screen()`
- `read_text_from_screen()`
- `detect_objects()`
- `narrate_scene()`

### Tech Stack
- `OpenCV`
- `Tesseract OCR`
- `YOLOv8`
- GPU (RTX 2050)

### Test Cases
| Query | Result |
|----|----|
What is on my screen | Spoken summary |
Read this page | OCR + TTS |
Is there a button | Spatial answer |

---

## 🟡 PHASE 5 — CONTEXT MEMORY  
**Status: ⏳ PLANNED**

### Goal
Make interaction **context-aware**

### Features
- Session memory
- Reference resolution
- Action repetition
- Error recovery

### Functions / Modules
- `store_last_action()`
- `resolve_reference("it")`
- `repeat_last_action()`

### Tech Stack
- Python dict / deque
- Optional SQLite

### Test Cases
| Input | Result |
|----|----|
Close it | Closes last app |
Do that again | Repeats action |

---

## 🟡 PHASE 6 — GESTURE INTERACTION  
**Status: ⏳ PLANNED**

### Goal
Enable **non-speaking users** and safety overrides

### Features
- Hand detection
- Simple symbolic gestures
- Emergency stop

### Functions / Modules
- `detect_hand()`
- `classify_gesture()`
- `gesture_override()`

### Tech Stack
- `MediaPipe Hands`
- `OpenCV`

### Test Cases
| Gesture | Result |
|----|----|
✋ Palm | Stop all actions |
👍 Confirm | Execute command |

---

## 🟡 PHASE 7 — EMOTION AWARENESS  
**Status: ⏳ PLANNED**

### Goal
Adapt behavior based on **user state**

### Features
- Facial emotion detection
- Voice stress analysis
- Cognitive load handling

### Functions / Modules
- `detect_emotion()`
- `analyze_voice_stress()`
- `modulate_response()`

### Tech Stack
- `MediaPipe Face Mesh`
- CNN (FER-2013)
- Audio prosody analysis

### Test Cases
| Condition | Behavior |
|----|----|
Stress + delete | Confirmation |
Fatigue | Short answers |

---

## 🔴 PHASE 8 — MULTIMODAL FUSION ENGINE (CORE)  
**Status: ⏳ PLANNED (MOST IMPORTANT)**

### Goal
Resolve conflicts and ensure **single safe action**

### Features
- Intent buffer
- Priority rules
- Mode enforcement
- Emotion-aware suppression
- Single-action guarantee

### Functions / Modules
- `add_intent()`
- `resolve_conflicts()`
- `select_final_action()`

### Tech Stack
- Pure Python logic
- Rule engine
- Optional ML later

### Test Cases
| Inputs | Result |
|----|----|
Voice delete + stress | Block |
Voice yes + gesture stop | Cancel |
Multiple inputs | One action |

---

## 🟡 PHASE 9 — ADAPTIVE LEARNING  
**Status: ⏳ PLANNED**

### Goal
Personalize assistant behavior

### Features
- Learn command preferences
- Learn confirmation tolerance
- Learn TTS speed

### Functions / Modules
- `update_preferences()`
- `adjust_tts_speed()`

### Tech Stack
- Rule-based learning
- Contextual bandits (optional)

### Test Cases
| Pattern | Result |
|----|----|
User says “browser” | Opens Chrome |
Repeated confirmations | Removed |

---

## 🟡 PHASE 10 — UI & ACCESSIBILITY PROFILES  
**Status: ⏳ PLANNED**

### Goal
Make system usable & demo-ready

### Features
- Minimal UI
- Voice-only mode
- Gesture-only mode
- Accessibility profiles

### Tech Stack
- `Tkinter` / `PyQt` / Web UI

### Test Cases
| Mode | Behavior |
|----|----|
Voice-only | No UI needed |
Gesture-only | Visual feedback |

---

## 🏁 FINAL NOTE

This project is:
- Major-project worthy
- Research & paper ready
- Resume flagship
- Assistive-technology focused

**Phase 1 is complete and stable.**  
Next development starts from **Phase 2 (Intent & Mode Engine)**.

---

## 🤝 CONTRIBUTION GUIDE

1. Clone repo
2. Create virtual environment
3. Run Phase-1
4. Implement next phase in order
5. Do NOT skip phases

---

> “Build intelligence only after safety is guaranteed.”