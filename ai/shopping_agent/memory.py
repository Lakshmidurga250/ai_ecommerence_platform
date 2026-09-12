"""
Conversational Session Memory for AI Shopping Agent.
Maintains multi-turn dialogue history, entity preferences, extracted requirements,
and session context with windowed memory and persistence.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import uuid


class ConversationTurn:
    """Represents a single exchange in a conversational shopping session."""
    def __init__(
        self,
        role: str,
        content: str,
        intent: Optional[str] = None,
        extracted_requirements: Optional[Dict[str, Any]] = None,
        tools_invoked: Optional[List[str]] = None,
        grounded_product_ids: Optional[List[int]] = None,
        timestamp: Optional[datetime] = None
    ):
        self.role = role  # "user" or "assistant"
        self.content = content
        self.intent = intent
        self.extracted_requirements = extracted_requirements or {}
        self.tools_invoked = tools_invoked or []
        self.grounded_product_ids = grounded_product_ids or []
        self.timestamp = timestamp or datetime.now(timezone.utc)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "role": self.role,
            "content": self.content,
            "intent": self.intent,
            "extracted_requirements": self.extracted_requirements,
            "tools_invoked": self.tools_invoked,
            "grounded_product_ids": self.grounded_product_ids,
            "timestamp": self.timestamp.isoformat()
        }


class ShoppingAgentMemory:
    """
    Session memory store maintaining active context per session ID.
    Tracks dialogue turns, cumulative preferences (preferred categories, brands, max budget, use cases),
    and active viewed products.
    """

    def __init__(self, session_id: Optional[str] = None, user_id: Optional[int] = None, max_history_turns: int = 12):
        self.session_id = session_id or str(uuid.uuid4())
        self.user_id = user_id
        self.max_history_turns = max_history_turns
        self.turns: List[ConversationTurn] = []
        self.cumulative_preferences: Dict[str, Any] = {
            "preferred_categories": [],
            "preferred_brands": [],
            "max_budget": None,
            "min_budget": None,
            "use_cases": [],
            "key_requirements": [],
            "negative_keywords": []
        }
        self.last_viewed_product_ids: List[int] = []
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def add_user_message(self, message: str, intent: Optional[str] = None, extracted_reqs: Optional[Dict[str, Any]] = None):
        """Record a user query turn and merge newly extracted requirements into cumulative preferences."""
        reqs = extracted_reqs or {}
        turn = ConversationTurn(
            role="user",
            content=message,
            intent=intent,
            extracted_requirements=reqs
        )
        self.turns.append(turn)
        self._merge_preferences(reqs)
        self._trim_history()
        self.updated_at = datetime.now(timezone.utc)

    def add_assistant_message(
        self,
        reply: str,
        intent: Optional[str] = None,
        tools_invoked: Optional[List[str]] = None,
        grounded_product_ids: Optional[List[int]] = None
    ):
        """Record an assistant reply turn with grounded products and invoked tools."""
        p_ids = grounded_product_ids or []
        turn = ConversationTurn(
            role="assistant",
            content=reply,
            intent=intent,
            tools_invoked=tools_invoked,
            grounded_product_ids=p_ids
        )
        self.turns.append(turn)
        if p_ids:
            for pid in p_ids:
                if pid not in self.last_viewed_product_ids:
                    self.last_viewed_product_ids.append(pid)
            self.last_viewed_product_ids = self.last_viewed_product_ids[-10:]
        self._trim_history()
        self.updated_at = datetime.now(timezone.utc)

    def _merge_preferences(self, reqs: Dict[str, Any]):
        """Accumulates long-term context across multi-turn exchanges."""
        if not reqs:
            return

        cat = reqs.get("category")
        if cat and cat not in self.cumulative_preferences["preferred_categories"]:
            self.cumulative_preferences["preferred_categories"].append(cat)

        brand = reqs.get("brand")
        if brand and brand not in self.cumulative_preferences["preferred_brands"]:
            self.cumulative_preferences["preferred_brands"].append(brand)

        if reqs.get("max_budget") is not None:
            self.cumulative_preferences["max_budget"] = reqs["max_budget"]
        if reqs.get("min_budget") is not None:
            self.cumulative_preferences["min_budget"] = reqs["min_budget"]

        use_case = reqs.get("use_case")
        if use_case and use_case not in self.cumulative_preferences["use_cases"]:
            self.cumulative_preferences["use_cases"].append(use_case)

        for req in reqs.get("requirements", []):
            if req not in self.cumulative_preferences["key_requirements"]:
                self.cumulative_preferences["key_requirements"].append(req)

    def _trim_history(self):
        """Maintains conversational sliding window without blowing context budget."""
        if len(self.turns) > self.max_history_turns * 2:
            self.turns = self.turns[:2] + self.turns[-(self.max_history_turns * 2 - 2):]

    def get_recent_history(self, limit: int = 6) -> List[Dict[str, Any]]:
        """Returns recent turns for LLM prompt assembly."""
        return [t.to_dict() for t in self.turns[-limit:]]

    def clear(self):
        """Reset memory for new conversation."""
        self.turns.clear()
        self.cumulative_preferences = {
            "preferred_categories": [],
            "preferred_brands": [],
            "max_budget": None,
            "min_budget": None,
            "use_cases": [],
            "key_requirements": [],
            "negative_keywords": []
        }
        self.last_viewed_product_ids.clear()
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "turn_count": len(self.turns),
            "cumulative_preferences": self.cumulative_preferences,
            "last_viewed_product_ids": self.last_viewed_product_ids,
            "recent_turns": self.get_recent_history(limit=8),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


# Global in-memory session manager for conversational persistence
class SessionMemoryRegistry:
    _sessions: Dict[str, ShoppingAgentMemory] = {}

    @classmethod
    def get_or_create(cls, session_id: Optional[str] = None, user_id: Optional[int] = None) -> ShoppingAgentMemory:
        if session_id and session_id in cls._sessions:
            mem = cls._sessions[session_id]
            if user_id and not mem.user_id:
                mem.user_id = user_id
            return mem

        new_id = session_id or str(uuid.uuid4())
        mem = ShoppingAgentMemory(session_id=new_id, user_id=user_id)
        cls._sessions[new_id] = mem
        return mem

    @classmethod
    def get_session(cls, session_id: str) -> Optional[ShoppingAgentMemory]:
        return cls._sessions.get(session_id)

    @classmethod
    def clear_session(cls, session_id: str) -> bool:
        if session_id in cls._sessions:
            cls._sessions[session_id].clear()
            return True
        return False
