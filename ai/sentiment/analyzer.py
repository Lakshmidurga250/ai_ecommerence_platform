"""
AI Review Sentiment Analysis Pipeline.
Computes real mathematical polarity (-1.0 to 1.0), subjectivity (0.0 to 1.0),
confidence scores, and extracts product aspect sentiments.
"""

import re
from typing import Dict, Any, List, Tuple

# Core Lexicon with polarity weights
LEXICON = {
    # Strong positive (+0.8 to +1.0)
    "excellent": 1.0, "outstanding": 1.0, "amazing": 0.95, "fantastic": 0.95,
    "perfect": 1.0, "awesome": 0.9, "superb": 0.9, "exceptional": 0.95,
    "love": 0.85, "loved": 0.85, "brilliant": 0.9, "flawless": 0.95,
    # Moderate positive (+0.4 to +0.7)
    "good": 0.6, "great": 0.75, "nice": 0.5, "fast": 0.5, "smooth": 0.6,
    "happy": 0.65, "pleased": 0.6, "durable": 0.7, "reliable": 0.75,
    "comfortable": 0.7, "value": 0.6, "worth": 0.65, "premium": 0.75,
    "satisfied": 0.6, "decent": 0.4, "solid": 0.5, "recommend": 0.7,
    # Slight positive (+0.2 to +0.3)
    "fine": 0.25, "ok": 0.2, "okay": 0.2, "acceptable": 0.3,
    # Negative (-0.4 to -0.7)
    "bad": -0.6, "poor": -0.7, "slow": -0.5, "rough": -0.5, "uncomfortable": -0.7,
    "cheap": -0.45, "disappointed": -0.75, "disappointing": -0.75, "issue": -0.4,
    "broken": -0.8, "flimsy": -0.65, "useless": -0.85, "defective": -0.8,
    "hate": -0.85, "terrible": -0.95, "horrible": -0.95, "awful": -0.95,
    "worst": -1.0, "waste": -0.9, "fraud": -1.0, "fake": -0.9
}

INTENSIFIERS = {
    "very": 1.4, "extremely": 1.7, "really": 1.3, "super": 1.4,
    "so": 1.25, "highly": 1.4, "absolutely": 1.6, "quite": 1.15
}

NEGATIONS = {"not", "never", "no", "hardly", "barely", "scarcely", "without", "didn't", "cannot", "won't", "don't"}

ASPECTS = {
    "quality": ["quality", "material", "build", "durability", "finish"],
    "battery": ["battery", "charge", "backup", "power"],
    "price": ["price", "cost", "value", "expensive", "affordable", "worth"],
    "performance": ["speed", "fast", "performance", "lag", "smooth"],
    "comfort": ["comfort", "comfortable", "fit", "wear", "size"],
    "delivery": ["delivery", "shipping", "packaging", "courier", "arrival"]
}


class SentimentAnalyzer:
    @staticmethod
    def analyze_text(text: str, extract_aspects: bool = True) -> Dict[str, Any]:
        """Analyzes review text and returns polarity, subjectivity, classification, and aspects."""
        if not text or not text.strip():
            return {
                "sentiment_label": "NEUTRAL",
                "polarity_score": 0.0,
                "subjectivity_score": 0.0,
                "confidence_score": 0.5,
                "extracted_aspects": {}
            }

        words = re.findall(r"\b\w+(?:'\w+)?\b", text.lower())
        total_score = 0.0
        scored_words_count = 0
        negate = False
        multiplier = 1.0

        for i, word in enumerate(words):
            if word in NEGATIONS:
                negate = not negate
                continue
            if word in INTENSIFIERS:
                multiplier = INTENSIFIERS[word]
                continue

            if word in LEXICON:
                base_weight = LEXICON[word]
                score = base_weight * multiplier
                if negate:
                    score = -score * 0.8
                total_score += score
                scored_words_count += 1
                negate = False
                multiplier = 1.0

        # Polarity normalized between -1.0 and 1.0
        if scored_words_count > 0:
            avg_score = total_score / scored_words_count
            polarity = max(-1.0, min(1.0, round(avg_score, 3)))
            confidence = min(0.98, round(0.65 + (scored_words_count * 0.05) + (abs(polarity) * 0.2), 3))
            subjectivity = min(1.0, round(scored_words_count / max(5, len(words) * 0.4), 3))
        else:
            polarity = 0.0
            confidence = 0.5
            subjectivity = 0.1

        # Classify label
        if polarity >= 0.15:
            label = "POSITIVE"
        elif polarity <= -0.15:
            label = "NEGATIVE"
        else:
            label = "NEUTRAL"

        # Aspect sentiment extraction
        aspect_sentiments = {}
        if extract_aspects:
            sentences = re.split(r"[.!?]+", text.lower())
            for sentence in sentences:
                sent_words = re.findall(r"\b\w+\b", sentence)
                for aspect_name, keywords in ASPECTS.items():
                    if any(kw in sent_words for kw in keywords):
                        sub_res = SentimentAnalyzer.analyze_text(sentence, extract_aspects=False)
                        aspect_sentiments[aspect_name] = sub_res["sentiment_label"].lower()

        return {
            "sentiment_label": label,
            "polarity_score": polarity,
            "subjectivity_score": subjectivity,
            "confidence_score": confidence,
            "extracted_aspects": aspect_sentiments
        }
