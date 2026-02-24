import pytesseract
import cv2
import re


class OCREngine:
    """
    Production OCR Engine (Clean & Stable)
    """

    def extract_text(self, frame):

        if frame is None:
            raise RuntimeError("Invalid frame for OCR")

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

        raw_text = pytesseract.image_to_string(gray)

        lines = raw_text.split("\n")
        cleaned_lines = []
        seen_lines = set()

        ui_noise_keywords = [
            "file edit view",
            "search",
            "utf-8",
            "windows",
            "plain text",
            "100%",
            "col",
            "ln",
            "recycle bin",
            "chrome",
        ]

        for line in lines:
            line = line.strip()

            if not line:
                continue

            if len(line) < 5:
                continue

            lower_line = line.lower()

            if any(keyword in lower_line for keyword in ui_noise_keywords):
                continue

            # 🔥 Remove leading 1-2 character token (like "Bs ")
            line = re.sub(r'^[A-Za-z]{1,2}\s+', '', line)

            if line in seen_lines:
                continue

            seen_lines.add(line)
            cleaned_lines.append(line)

        final_text = "\n".join(cleaned_lines)

        return final_text.strip()