"""
Review Quality & Spam Detection Engine.
Assesses informational depth, lexical richness, sentiment-rating alignment,
and bot/spam heuristics to score customer review authenticity and quality.
"""
from typing import Dict, Any, List
import re
import math


class ReviewQualityDetector:
    """
    Evaluates review text quality, depth, and spam probability.
    """

    SPAM_PATTERNS = [
        r"http[s]?://\S+",             # Links/URLs
        r"whatsapp",                   # Off-platform contact
        r"call\s+me",                  # Contact solicitations
        r"discount\s+code",            # External affiliate promo
        r"free\s+money",
        r"(.)\1{4,}",                  # Repetitive characters e.g. "greeeeaaat"
    ]

    def evaluate_review_quality(
        self,
        comment: str,
        rating: int,
        is_verified_purchase: bool = True
    ) -> Dict[str, Any]:
        """
        Calculates quality score (0-100) and spam classification for a customer review.
        """
        text = (comment or "").strip()
        flags = []
        is_spam = False

        if not text:
            return {
                "quality_score": 10.0,
                "quality_tier": "EMPTY_OR_BLANK",
                "is_spam": False,
                "is_helpful": False,
                "flags": ["No review text provided"],
                "word_count": 0,
                "lexical_richness": 0.0
            }

        # 1. Regex Spam Check
        for pat in self.SPAM_PATTERNS:
            if re.search(pat, text, re.IGNORECASE):
                flags.append("Contains suspicious link, contact, or repetitive spam pattern")
                is_spam = True
                break

        # 2. Length & Informational Depth
        words = re.findall(r"\b\w+\b", text.lower())
        word_count = len(words)
        char_count = len(text)

        if word_count < 4:
            flags.append("Low informational depth (under 4 words)")
            length_score = 25.0
        elif word_count < 12:
            length_score = 55.0
        elif word_count < 40:
            length_score = 85.0
        else:
            length_score = 100.0

        # 3. Lexical Richness (Unique words ratio)
        unique_words = len(set(words))
        lexical_richness = round(unique_words / max(1, word_count), 2)
        if lexical_richness < 0.40 and word_count > 10:
            flags.append("High repetitive phrasing / low lexical diversity")
            diversity_score = 30.0
        else:
            diversity_score = min(100.0, lexical_richness * 110.0)

        # 4. Rating vs Sentiment Alignment
        # Check for obvious discrepancy: 5-star with "worst/terrible/broken", or 1-star with "best/amazing/love"
        extreme_positive = bool(re.search(r"\b(best|amazing|excellent|love|perfect|fantastic)\b", text, re.I))
        extreme_negative = bool(re.search(r"\b(worst|terrible|horrible|broken|fake|scam|waste)\b", text, re.I))

        alignment_score = 100.0
        if rating >= 4 and extreme_negative and not extreme_positive:
            flags.append("Rating-sentiment contradiction (High rating with strongly negative keywords)")
            alignment_score = 40.0
        elif rating <= 2 and extreme_positive and not extreme_negative:
            flags.append("Rating-sentiment contradiction (Low rating with strongly positive keywords)")
            alignment_score = 40.0

        # 5. Verified Purchase Weight
        verification_bonus = 15.0 if is_verified_purchase else -10.0

        # Composite Quality Score (0 to 100)
        raw_score = (
            0.40 * length_score +
            0.30 * diversity_score +
            0.30 * alignment_score +
            verification_bonus
        )

        if is_spam:
            raw_score = min(15.0, raw_score)

        final_score = round(max(0.0, min(100.0, raw_score)), 1)

        if final_score >= 80.0:
            tier = "HIGH_QUALITY_DETAILED"
            is_helpful = True
        elif final_score >= 50.0:
            tier = "ACCEPTABLE_STANDARD"
            is_helpful = True
        elif final_score >= 25.0:
            tier = "LOW_EFFORT_MINIMAL"
            is_helpful = False
        else:
            tier = "SUSPICIOUS_SPAM"
            is_helpful = False
            is_spam = True

        return {
            "quality_score": final_score,
            "quality_tier": tier,
            "is_spam": is_spam,
            "is_helpful": is_helpful,
            "word_count": word_count,
            "char_count": char_count,
            "lexical_richness": lexical_richness,
            "is_verified_purchase": is_verified_purchase,
            "flags": flags or ["Valid authentic review text"]
        }
