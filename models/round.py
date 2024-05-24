"""
Gets data from the tournaments.py and then creates the rounds

Rounds take the match and then gives it to match again and so on.
"""

from typing import List, Optional
from .match import Match

class Round:
    def __init__(self, matches: List[Match]):
        self.matches = matches

    def __repr__(self):
        return f"Round(matches={self.matches})"

    @classmethod
    def deserialize(cls, data):
        matches = [Match.deserialize(match_data) for match_data in data]
        return cls(matches=matches)