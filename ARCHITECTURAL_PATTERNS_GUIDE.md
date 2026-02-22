# Intent Parsing, Mode Detection & Safety Rules - Architectural Analysis

## Executive Summary

Analysis of 3 major open-source AI assistant projects reveals consistent architectural patterns for:
1. **Intent Representation** - How user intentions are modeled
2. **Confidence Scoring** - Multi-level verification strategies
3. **Safety Implementation** - Constraint-based ACL patterns
4. **State Management** - Layered finite state machines
5. **Entity Recognition** - Keyword + regex + fuzzy matching hybrid

---

## 1. Mycroft AI - Voice Assistant Patterns

### Intent Architecture

**IntentBuilder Pattern** (Fluent DSL):
```python
IntentBuilder('weather_intent') \
    .require('WeatherKeyword') \
    .optionally('LocationKeyword') \
    .build()
```

**Key Classes:**
- `IntentBuilder` - Fluent intent definition
- `AdaptIntent` - Extends IntentBuilder with empty name default
- `IntentMatch` - Result wrapper: `IntentMatch(service, intent_type, intent_data, skill_id)`

### Confidence Scoring Strategy

**Three-Tier System** via `PadatiousMatcher`:
```python
HIGH_CONFIDENCE = 0.95   # Match immediately
MEDIUM_CONFIDENCE = 0.8  # Execute with confirmation
LOW_CONFIDENCE = 0.5     # Ask for clarification
```

**Matching Priority Order:**
1. `padatious_matcher.match_high()` - Neural network (0.95+)
2. `adapt_service.match_intent()` - Keyword-based
3. `padatious_matcher.match_medium()` - Neural (0.8+)
4. `padatious_matcher.match_low()` - Neural (0.5+)

**Best Match Selection:**
```python
best_intent = max(intents, key=lambda x: x.get('confidence', 0.0))
```

### Entity Extraction Methods

**Three Approaches:**

1. **Vocabulary Keywords** (`.voc` files):
   ```
   hello|hi|greetings
   weather information|weather|forecast
   ```
   Registration: `register_vocabulary('hello', 'GreetingKeyword')`

2. **Regex Patterns** (`.rx` files):
   ```
   set (?P<DeviceName>\w+) to (?P<Level>\d+)%
   ```
   Registration: `register_regex(regex_pattern)`

3. **Context Manager** (Implicit extraction):
   - Maintains frame stack with timeout
   - `ContextManager(max_frames=3, timeout=2)`
   - Greedy vs. selective entity injection modes

### Context Management

```python
class ContextManager:
    frame_stack: list[ContextManagerFrame]  # Max 3 frames by default
    timeout: int = 2  # seconds
    max_frames: int = 3
    greedy: bool = False  # If true, always inject; else selective
```

---

## 2. Home Assistant - Automation & Intent System

### Intent Model (Event-Driven)

**Core Intent Structure:**
```python
class Intent:
    intent_type: str              # e.g., 'HassTurnOn'
    slots: dict[str, SlotInfo]    # Extracted parameters
    device_id: str | None         # Target device
    context: Context              # Source tracking
    platform: str                 # e.g., 'hassil', 'alexa'
    language: str                 # e.g., 'en-us'
```

**Predefined Intents:**
- `INTENT_TURN_ON / INTENT_TURN_OFF` - Power control
- `INTENT_TOGGLE` - State toggle
- `INTENT_SET_POSITION` - Sliding control
- `INTENT_GET_STATE` - Query entities
- `INTENT_START_TIMER` - Timer management

### Constraint-Based Matching

**MatchTargetsConstraints** (Layered validation):
```python
constraints = MatchTargetsConstraints(
    name='bedroom light',           # Entity name fuzzy match
    area_name='bedroom',            # Area filter
    floor_name='second_floor',      # Floor filter
    domains={'light', 'switch'},    # Required domain
    device_classes={'brightness'},  # Device class filter
    features=SUPPORT_BRIGHTNESS,    # Feature bitmask
    states={'on', 'off'},           # Required states
    assistant='alexa',              # Platform filter
    single_target=True              # Exactly one match
)
```

**Sequential Filtering Algorithm** (`async_match_targets`):
1. All entities of required domain
2. Filter by device class
3. Filter by feature support
4. Filter by state requirements
5. Match by name/alias
6. Apply area/floor preferences

### Finite State Machine - Automation

**States:**
- `ENABLED` → Automation active and listening
- `DISABLED` → Automation inactive
- `TRIGGERED` → Trigger fired, checking conditions
- `RUNNING_ACTION` → Executing action script
- `IDLE` → Awaiting next trigger

**State Transitions:**
```
TRIGGERED → [Check Conditions]
           ├─ Conditions Met → RUNNING_ACTION → IDLE
           └─ Conditions Failed → Abort, return to IDLE
```

**Trace System** (FSM audit trail):
- Every state transition captured
- Conditions and actions traced
- Enables debugging and review

### Safety Rules - Constraint-Based ACL

**Example: Turn Light On Intent**
```python
# Required constraints for safe execution
required_domains = {'light'}  # Only light entities
required_features = SUPPORT_TURN_ON  # Must support turn_on
device_classes = {'brightness', 'dimmer', 'switch'}  # Allowed device types

# Execute only if ALL constraints met
if not match_result.is_match:
    raise MatchFailedError(result, constraints)
```

**Failure Handling:**
```python
try:
    await service_call(domain, service, intent_obj, state)
except Exception:
    failed_results.append(target)

if not success_results:
    raise IntentHandleError(f"Failed to call {service}")
```

---

## 3. Open-Assistant - Safety-First Design

### Message Tree State Machine

**Workflow Stages:**
```
INITIAL_PROMPT_REVIEW
    ├─ [Spam check] → ABORTED_LOW_GRADE (if spam)
    └─ [Approve] → GROWING

GROWING (Collect responses)
    ├─ [Enough responses + good quality] → RANKING
    └─ [Too many poor responses] → ABORTED_LOW_GRADE

RANKING (Compare alternatives)
    └─ [Ranking complete] → READY_FOR_SCORING

READY_FOR_SCORING (Prepare for models)
    ├─ [Pass evaluator models] → READY_FOR_EXPORT
    └─ [Fail quality tests] → ABORTED_LOW_GRADE

READY_FOR_EXPORT (Approved dataset)
HALTED_BY_MODERATOR (Manual intervention)
BACKLOG_RANKING (Pending ranking tasks)
```

### Safety Parameters & Levels

**Tiered Safety System (0-9 Scale):**

```python
class SafetyParameters:
    level: int  # 0-9, validated with @pydantic.validator
    
    # Safety triggering logic
    TRIGGER_LOGIC = (
        ("caution" in label and level > 1) or 
        ("intervention" in label and level > 0)
    )
```

**Safety Labels:**
- `__casual__` - No safety concern
- `__possibly_needs_caution__` - Minor concern
- `__probably_needs_caution__` - Moderate concern
- `__needs_caution__` - Significant concern
- `__needs_intervention__` - Critical follow-up needed

### Rules of Thumbs (ROTs) Pattern

**Safety Response Format:**
```python
class SafePromptResponse:
    safe_prompt: str         # Modified prompt with instructions
    safety_label: str        # Classification
    safety_rots: str         # Rules of thumbs guidance
    safety_parameters: SafetyParameters
```

**ROTs Generation:**
```python
def prepare_safe_prompt(prompt: str, label: str, rots: str):
    instruction = f"Answer with {label} as responsible chatbot that believes {rots}: "
    return instruction + prompt
```

### Message State Tracking

**MessageState Enum:**
```python
STATES = [
    'manual' - User-created,
    'pending' - Queued for worker,
    'in_progress' - Being generated,
    'complete' - Successfully generated,
    'aborted_by_worker' - Worker error,
    'cancelled' - User cancelled,
    'timeout' - Generation timeout
]
```

**State Transitions:**
```
pending → in_progress → complete
                    ├─ aborted_by_worker
                    └─ timeout
any_state → cancelled (user action)
```

---

## 4. Comparative Pattern Analysis

### Intent Representation

| Framework | Approach | Structure |
|-----------|----------|-----------|
| **Mycroft** | Rule-based + Neural | IntentBuilder DSL → IntentMatch |
| **Home Assistant** | Constraint-based targeting | Intent w/ slots → MatchTargetsResult |
| **OpenAssistant** | Implicit via role + task | Message role/state + task type |
| **Recommendation** | Hybrid layered | Multiple parsers with fallback |

### Confidence Scoring

| Framework | Method | Thresholds |
|-----------|--------|------------|
| **Mycroft** | Neural ML + keyword matching | 0.95/0.8/0.5 fixed |
| **Home Assistant** | Constraint validation score | Domain × Feature × State |
| **OpenAssistant** | Safety model classification | 0-9 safety levels |
| **Recommendation** | Multi-factor scoring | High (0.95) → Medium (0.8) → Low (0.5) |

### Safety Implementation

| Framework | Approach | Mechanism |
|-----------|----------|-----------|
| **Mycroft** | Skill-delegated | Context + enable/disable per skill |
| **Home Assistant** | Constraint ACL | Domain/Feature/Capability matching |
| **OpenAssistant** | Label-based classification | Safety level + ROTs guidance |
| **Recommendation** | Hierarchical | ACL → Confidence → Safety Labels |

### State Machine Complexity

| Framework | Pattern | Depth |
|-----------|---------|-------|
| **Mycroft** | Active skills tracking | 1 level (skill state) |
| **Home Assistant** | Automation trigger→action | 2 levels (enabled + trigger-action) |
| **OpenAssistant** | Message workflow | 2 levels (message state + tree state) |
| **Recommendation** | Layered FSM | 3+ levels (mode + intent + safety) |

---

## 5. Recommended Implementation Architecture

### Multi-Service Intent Hierarchy

```
[User Input]
     ↓
[1. Fast Loop] - Keyword trie & regex
     ├─ Match found (0.95+) → [Execute]
     └─ No match → [2. Medium Loop]
          ↓
[2. Medium Loop] - ML-based classifier
     ├─ Match found (0.8+) → [Ask Confirmation]
     └─ No match → [3. Slow Loop]
          ↓
[3. Slow Loop] - Contextual reasoing
     ├─ Match found (0.5+) → [Ask Clarification]
     └─ No match → [Fallback Handler]
```

### Confidence-Action Mapping

```python
if confidence >= 0.95:
    action = EXECUTE_IMMEDIATELY
elif confidence >= 0.8:
    action = EXECUTE_WITH_CONFIRMATION
elif confidence >= 0.5:
    action = ASK_FOR_CLARIFICATION
elif confidence >= 0.3:
    action = PROVIDE_SUGGESTIONS
else:
    action = REJECT_AND_RETRY
```

### Layered Safety State Machine

```
STATE: Safety Unchecked
  ├─ Apply ACL (domain, feature, capability)
  └─ STATE: Safety Checked
       ├─ Safety level 0-2: Auto-approve
       ├─ Safety level 3-6: Confidence required (0.8+)
       └─ Safety level 7-9: Specialist review
            └─ STATE: Safety Approved
                 └─ [Execute Action]
```

### Entity Recognition Hierarchy

```
1. Exact Keyword Match
   - O(1) trie lookup
   - 0.99 confidence

2. Fuzzy Name Match  
   - Levenshtein distance on entity names
   - 0.85-0.95 confidence

3. Regex Pattern
   - Named group extraction
   - 0.7-0.85 confidence

4. Context Inference
   - Historical references
   - 0.5-0.7 confidence
```

---

## 6. Key Design Principles Identified

### 1. **Multi-Service Redundancy**
- Mycroft: Adapt (keywords) + Padatious (neural) + Fallback
- Home Assistant: Constraints + slot extraction
- OpenAssistant: Safety + state + task type
- **Principle**: Never single point of failure

### 2. **Confidence-Gated Execution**
- Different actions at different confidence levels
- No action without sufficient confidence floor
- Confirmation required at medium confidence

### 3. **Constraint-Based Access Control**
- Home Assistant model most explicit
- ACL before intent classification
- Feature validation before execution

### 4. **State Tracing & Auditability**
- Home Assistant trace system captures every step
- OpenAssistant tracks message & tree state
- Critical for debugging and safety review

### 5. **Context as First-Class Concept**
- Mycroft: Explicit ContextManager
- Home Assistant: Implicit in state tracking
- OpenAssistant: Message history as context

### 6. **Mode/State Orthogonality**
- Conversation mode independent of safety
- Voice/text independent of automation
- Allows mixing strategies

---

## 7. Implementation Recommendations

### For Your Multimodal Assistant

```python
class IntentParser:
    def parse(utterance, context):
        # Layer 1: Fast keyword matching
        match = keyword_trie.match(utterance)
        if match and match.confidence > 0.95:
            return IntentMatch(match, confidence=0.95)
        
        # Layer 2: ML classifier
        ml_match = classifier.predict(utterance)
        if ml_match.confidence > 0.8:
            return IntentMatch(ml_match, requires_confirmation=True)
        
        # Layer 3: Context-aware inference
        context_match = context_reasoner.infer(utterance, context)
        if context_match.confidence > 0.5:
            return IntentMatch(context_match, requires_clarification=True)
        
        return None

class SafetyValidator:
    def validate(intent, safety_level):
        # ACL check
        if not acl.check(intent.domain, intent.features):
            raise PermissionError()
        
        # Confidence gating
        if safety_level >= 7 and intent.confidence < 0.95:
            raise InsufficientConfidenceError()
        
        # Safety label check
        if safety_level >= 3 and "intervention" in intent.safety_label:
            require_specialist_review()
        
        return True
```

---

## References

- **Mycroft AI**: Intent Service with Adapt + Padatious
- **Home Assistant**: Automation & Intent Handler System
- **OpenAssistant**: Safety System & Message Tree FSM
- **Key Files**:
  - `mycroft/skills/intent_service.py`
  - `homeassistant/helpers/intent.py`
  - `homeassistant/components/automation/__init__.py`
  - `oasst_shared/oasst_shared/schemas/inference.py`
