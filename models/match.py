from models import Player


class Match:
    def __init__(self, player1, player2=None, completed=False, result=None):
        self.player1 = player1
        self.player2 = player2
        self.completed = completed
        self.result = result

    def set_result(self, result):
        self.result = result
        self.completed = True

    def to_dict(self):
        return {
            "players": [self.player1.chess_id, self.player2.chess_id if self.player2 else None],
            "completed": self.completed,
            "winner": self.result
        }
