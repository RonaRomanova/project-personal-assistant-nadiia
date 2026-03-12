from dataclasses import dataclass, field
from datetime import datetime
from typing import List

@dataclass
class Note:
    """
    Клас для зберігання та керування нотатками.
    """
    id: int
    text: str
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    
    def matches(self, query: str) -> bool:
        """ Пошук по тексту або тегам. """
        q = query.lower()
        return q in self.text.lower() or any(q in t.lower() for t in self.tags)