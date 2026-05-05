from dataclasses import dataclass, field
from typing import List, Set, Optional
import uuid

@dataclass
class Player:
    name: str
    email: str
    chess_id: str  # Format: AB12345 (National Chess Identifier)
    birthdate: str
    rating: int = 1200
    score: float = 0.0
    opponents: Set[str] = field(default_factory=set)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "chess_id": self.chess_id,
            "birthdate": self.birthdate,
            "rating": self.rating,
            "score": self.score,
            "opponents": list(self.opponents),
        }

    @classmethod
    def from_dict(cls, d):
        opps = set(d.get("opponents", []))
        return cls(
            name=d["name"],
            email=d["email"],
            chess_id=d["chess_id"],
            birthdate=d["birthdate"],
            rating=d.get("rating", 1200),
            score=d.get("score", 0.0),
            opponents=opps,
            id=d.get("id", str(uuid.uuid4()))
        )

@dataclass
class Match:
    p1: Player
    p2: Player
    s1: Optional[float] = None
    s2: Optional[float] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def set_result(self, s1: float, s2: float):
        """Updates scores and tracks opponents played."""
        self.s1 = s1
        self.s2 = s2
        self.p1.score += s1
        self.p2.score += s2
        self.p1.opponents.add(self.p2.chess_id)
        self.p2.opponents.add(self.p1.chess_id)

    def to_dict(self):
        return {
            "p1_id": self.p1.chess_id,
            "p2_id": self.p2.chess_id,
            "s1": self.s1,
            "s2": self.s2
        }

class Round:
    def __init__(self, name: str):
        self.name = name
        self.matches: List[Match] = []

    def to_dict(self):
        return {
            "name": self.name,
            "matches": [m.to_dict() for m in self.matches]
        }

@dataclass
class Tournament:
    name: str
    venue: str
    start_date: str
    end_date: str
    total_rounds: int = 4
    current_round: int = 1
    players: List[Player] = field(default_factory=list)
    rounds: List[Round] = field(default_factory=list)
    completed: bool = False
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def add_player(self, p: Player):
        self.players.append(p)

    def standings(self):
        """Sorts players by score (desc) then rating (desc)."""
        return sorted(self.players, key=lambda x: (-x.score, -x.rating))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "venue": self.venue,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "total_rounds": self.total_rounds,
            "current_round": self.current_round,
            "completed": self.completed,
            "players": [p.to_dict() for p in self.players],
            "rounds": [r.to_dict() for r in self.rounds]
        }

class Club:
    def __init__(self, name: str):
        self.name = name
        self.players: List[Player] = []

    def to_dict(self):
        return {
            "name": self.name,
            "players": [p.to_dict() for p in self.players]
        }