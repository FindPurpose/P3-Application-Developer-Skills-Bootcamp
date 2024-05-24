import json
from .player import Player

"""
    Would first make a match. 
    Randomize who wins and who loses. 
    After that Send that to the round
    """
from typing import List, Optional
import random
class Match:
    def __init__(self, players, completed=False,  result=None):
        self.player1, self.player2 = players
        self.result = result 
        self.completed = completed

    def set_result(self, result):
        self.result = result
        self.completed = True
        if result == 'player1':
            self.player1.points += 1
        elif result == 'player2':
            self.player2.points += 1
        elif result == 'draw':
            self.player1.points += 0.5
            self.player2.points += 0.5

    def __repr__(self):
        return f"Match({self.player1.chess_id} vs {self.player2.chess_id}, result={self.result})"

    @classmethod
    def deserialize(cls, data):
        return cls(
            players=data["players"],
            completed=data["completed"],
            winner=data.get("winner")
        )