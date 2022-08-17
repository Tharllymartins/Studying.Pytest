from dataclasses import dataclass


@dataclass
class DeckModel:
    success: bool
    deck_id: str
    remaining: int
    shuffled: bool
    