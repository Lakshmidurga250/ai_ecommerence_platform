"""
AI Natural Language Query Intent Parser & Attribute Extractor.
Extracts structured parameters (Color, Category, Brand, Max Price, Min Rating) from conversational user search queries.
"""

import re
from typing import Dict, Any, Optional

COLORS = ["black", "white", "blue", "red", "green", "grey", "gray", "silver", "gold", "yellow", "navy", "pink", "purple", "brown"]

CATEGORIES = [
    "running shoes", "shoes", "sneakers", "boots", "sandals", "footwear",
    "laptop", "laptops", "smartphone", "smartphones", "phone", "phones",
    "headphones", "earphones", "earbuds", "audio", "smartwatch", "watches",
    "t-shirt", "tshirt", "shirt", "jeans", "jacket", "clothing", "apparel",
    "backpack", "bag", "camera", "tablet", "monitor", "keyboard"
]

BRANDS = ["apple", "samsung", "nike", "adidas", "sony", "dell", "hp", "lenovo", "puma", "boat", "noise", "lg"]


class QueryIntentParser:
    @staticmethod
    def parse_query(raw_query: str) -> Dict[str, Any]:
        """Parses conversational natural language queries into structured intent."""
        text = raw_query.lower().strip()
        cleaned_words = text.split()

        extracted_category = None
        extracted_brand = None
        extracted_color = None
        max_price = None
        min_rating = None
        extracted_attributes = {}

        # 1. Price extraction: "under 3000", "below 50k", "< 2000", "less than 1500"
        price_patterns = [
            r"(?:under|below|less than|within|<|<=)\s*(?:rs\.?|inr|₹)?\s*(\d+(?:,\d+)*(?:\.\d+)?)\s*(k|thousand)?",
            r"(?:rs\.?|inr|₹)\s*(\d+(?:,\d+)*(?:\.\d+)?)"
        ]
        for pattern in price_patterns:
            match = re.search(pattern, text)
            if match:
                val_str = match.group(1).replace(",", "")
                val = float(val_str)
                if match.lastindex >= 2 and match.group(2) in ("k", "thousand"):
                    val *= 1000.0
                max_price = val
                break

        # 2. Rating extraction: "top rated", "best", "4 star", "above 4.5"
        if "top rated" in text or "best" in text or "highly rated" in text:
            min_rating = 4.0
        rating_match = re.search(r"(\d(?:\.\d)?)\s*(?:star|\+)", text)
        if rating_match:
            min_rating = float(rating_match.group(1))

        # 3. Color extraction
        for color in COLORS:
            if re.search(r"\b" + color + r"\b", text):
                extracted_color = color
                extracted_attributes["color"] = color
                break

        # 4. Brand extraction
        for brand in BRANDS:
            if re.search(r"\b" + brand + r"\b", text):
                extracted_brand = brand
                break

        # 5. Category extraction
        for cat in CATEGORIES:
            if cat in text:
                extracted_category = cat
                break

        # Remove parsed tokens from cleaned query
        cleaned = text
        for token in [extracted_color, extracted_brand, extracted_category]:
            if token:
                cleaned = re.sub(r"\b" + re.escape(token) + r"\b", "", cleaned)
        cleaned = re.sub(r"(?:under|below|less than|rs\.?|inr|₹|\d+k?|star|\+)", "", cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        is_semantic = bool(extracted_color or max_price or min_rating or extracted_category or extracted_brand)

        return {
            "raw_query": raw_query,
            "cleaned_query": cleaned or raw_query,
            "extracted_category": extracted_category,
            "extracted_brand": extracted_brand,
            "extracted_color": extracted_color,
            "max_price": max_price,
            "min_rating": min_rating,
            "extracted_attributes": extracted_attributes,
            "is_semantic_intent": is_semantic
        }
