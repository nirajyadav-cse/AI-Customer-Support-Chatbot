"""Simple retrieval-based customer support chatbot."""
from pathlib import Path
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

KB_PATH = Path(__file__).parent / "data" / "knowledge_base.csv"

class SupportChatbot:
    def __init__(self, knowledge_base=None):
        self.kb = pd.read_csv(knowledge_base or KB_PATH).fillna("")
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
        self.documents = (self.kb["question"] + " " + self.kb["category"] + " " + self.kb["topic"]).astype(str)
        self.matrix = self.vectorizer.fit_transform(self.documents)

    def respond(self, message, threshold=0.12):
        message = str(message).strip()
        if not message:
            return {
                "answer": "Please type a question so I can try to help.",
                "topic": "Empty message", "confidence": 0.0, "escalate": False
            }
        query = self.vectorizer.transform([message])
        scores = cosine_similarity(query, self.matrix).ravel()
        best = int(scores.argmax())
        score = float(scores[best])
        if score < threshold:
            return {
                "answer": "I'm sorry, I couldn't find a reliable answer in my support guide. Please use **Contact human support** so a support representative can help you.",
                "topic": "Needs human support", "confidence": score, "escalate": True
            }
        answer = str(self.kb.iloc[best]["answer"])
        return {
            "answer": answer,
            "topic": str(self.kb.iloc[best]["topic"]),
            "confidence": score,
            "escalate": False
        }

def load_knowledge_base():
    return pd.read_csv(KB_PATH).fillna("")
