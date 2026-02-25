import time
import math


class EventEngine:

    def __init__(self,
                 cooldown=3.5,
                 motion_threshold=80):

        self.cooldown = cooldown
        self.motion_threshold = motion_threshold

        # 🔥 Only narrate important objects
        self.priority_objects = {
            "person",
            "phone",
            "chair",
            "door",
            "laptop"
        }

        self._last_spoken_time = 0
        self._last_event_signature = None

    # =====================================================

    def process_events(self, events, frame_width=None):

        current_time = time.time()

        if not events:
            return None

        for event in events:

            obj = event["object"]
            label = obj["label"]
            event_type = event["type"]

            # 🔴 Ignore non-priority objects
            if label not in self.priority_objects:
                continue

            signature = f"{event_type}_{obj['id']}"

            # 🔴 Prevent repeated same event
            if signature == self._last_event_signature:
                continue

            # 🔴 Cooldown protection
            if current_time - self._last_spoken_time < self.cooldown:
                continue

            # -------------------------------------------------
            # ENTRY
            # -------------------------------------------------

            if event_type == "ENTRY":

                message = self._format_with_position(
                    f"A {label} entered the scene.",
                    obj,
                    frame_width
                )

            # -------------------------------------------------
            # EXIT
            # -------------------------------------------------

            elif event_type == "EXIT":

                message = f"The {label} left the scene."

            # -------------------------------------------------
            # MOTION (only strong movement)
            # -------------------------------------------------

            elif event_type == "MOTION":

                vx, vy = obj["velocity"]
                motion = math.sqrt(vx ** 2 + vy ** 2)

                if motion < self.motion_threshold:
                    continue

                message = self._format_with_position(
                    f"The {label} moved significantly.",
                    obj,
                    frame_width
                )

            else:
                continue

            # Save state
            self._last_spoken_time = current_time
            self._last_event_signature = signature

            return message

        return None

    # =====================================================

    def _format_with_position(self, base_message, obj, frame_width):

        if not frame_width:
            return base_message

        x1, _, x2, _ = obj["bbox"]
        center_x = (x1 + x2) / 2

        zone = self._get_zone(center_x, frame_width)

        return f"{base_message} It is on your {zone}."

    # =====================================================

    def _get_zone(self, x, width):

        third = width / 3

        if x < third:
            return "left"
        elif x < 2 * third:
            return "center"
        else:
            return "right"