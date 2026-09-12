"""
AI Shopping Agent Package.
Autonomous conversational commerce, tool dispatch, multi-turn session memory,
grounding guardrails, response evaluation, and analytics telemetry.
"""

from ai.shopping_agent.agent import AIShoppingAgent
from ai.shopping_agent.memory import ShoppingAgentMemory, SessionMemoryRegistry
from ai.shopping_agent.guardrails import ShoppingAgentGuardrails
from ai.shopping_agent.evaluator import ResponseEvaluator
from ai.shopping_agent.analytics import ConversationAnalytics
from ai.shopping_agent.tools import (
    SearchAndFilterTool, ProductComparisonTool, CartActionTool,
    WishlistActionTool, OrderLookupTool, AlternativeAndBundleTool
)

__all__ = [
    "AIShoppingAgent",
    "ShoppingAgentMemory",
    "SessionMemoryRegistry",
    "ShoppingAgentGuardrails",
    "ResponseEvaluator",
    "ConversationAnalytics",
    "SearchAndFilterTool",
    "ProductComparisonTool",
    "CartActionTool",
    "WishlistActionTool",
    "OrderLookupTool",
    "AlternativeAndBundleTool"
]
