from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class MemoryEntry:
    """Single memory entry storing a user question and the associated result."""
    question: str
    result: Dict[str, Any]


@dataclass
class MemoryStore:
    """
    Lightweight in-memory store for agent interactions.
    This is intentionally simple and kept in-process.
    """
    history: List[MemoryEntry] = field(default_factory=list)

    def add_entry(self, question: str, result: Dict[str, Any]) -> None:
        """Append a new question/result pair to the memory history."""
        self.history.append(MemoryEntry(question=question, result=result))

    def get_history(self) -> List[MemoryEntry]:
        """Return the full interaction history."""
        return list(self.history)

    def last(self) -> Optional[MemoryEntry]:
        """Return the most recent memory entry, if any."""
        if not self.history:
            return None
        return self.history[-1]
