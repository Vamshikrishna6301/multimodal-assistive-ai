from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from typing import List, Tuple


class NeuralIntentClassifier:
    """
    Semantic intent classifier using embedding similarity.
    Used as fallback when rule-based parser confidence is low.
    """

    def __init__(self):

        print("🧠 Loading Neural Intent Classifier...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.intent_phrases = {
            "OPEN_APP": [
                "open chrome",
                "launch browser",
                "start application",
                "open my app",
            ],
            "CLOSE_APP": [
                "close application",
                "terminate app",
                "exit current app",
            ],
            "SWITCH_APP": [
                "switch window",
                "go to next app",
                "alt tab",
            ],
            "MINIMIZE_WINDOW": [
                "minimize window",
                "hide this window",
            ],
            "FOCUS_WINDOW": [
                "focus this window",
                "bring this to front",
            ],
            "TYPE_TEXT": [
                "type something",
                "write text",
                "enter text",
            ],
            "DICTATE_MODE": [
                "start dictation",
                "enable dictation mode",
            ],
            "SEND_MESSAGE": [
                "send a message",
                "send text message",
            ],
            "COPY_PASTE": [
                "copy this",
                "paste here",
            ],
            "OPEN_FILE": [
                "open file",
                "open document",
            ],
            "CREATE_FILE": [
                "create file",
                "new document",
            ],
            "DELETE_FILE": [
                "delete file",
                "remove document",
            ],
            "DOWNLOAD_FILE": [
                "download file",
                "save from internet",
            ],
            "OPEN_BROWSER": [
                "open browser",
                "start chrome",
            ],
            "SEARCH_WEB": [
                "search the internet",
                "look up online",
            ],
            "SCROLL_UP_DOWN": [
                "scroll down",
                "scroll up",
            ],
            "VOLUME_CONTROL": [
                "increase volume",
                "lower volume",
                "mute sound",
            ],
            "SCREEN_ZOOM_CONTROL": [
                "zoom in",
                "zoom out",
            ],
            "ENABLE_SCREEN_READER": [
                "enable narrator",
                "turn on screen reader",
            ]
        }

        self._build_index()
        print("✅ Neural Intent Classifier Ready")

    def _build_index(self):

        self.labels = []
        phrases = []

        for label, examples in self.intent_phrases.items():
            for example in examples:
                self.labels.append(label)
                phrases.append(example)

        embeddings = self.model.encode(phrases)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(np.array(embeddings).astype("float32"))

    def classify(self, text: str) -> Tuple[str, float]:

        embedding = self.model.encode([text])
        D, I = self.index.search(np.array(embedding).astype("float32"), k=1)

        similarity_score = float(1 / (1 + D[0][0]))
        predicted_label = self.labels[I[0][0]]

        return predicted_label, similarity_score