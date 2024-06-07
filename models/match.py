class Match:
    def __init__(self, player1, player2, completed=False, result=None):
        self.player1 = player1
        self.player2 = player2
        self.completed = completed
        self.result = result
    
    def set_result(self, result):
        if result not in (self.player1.chess_id, self.player2.chess_id, 'draw'):
            raise ValueError(f"Result must be {self.player1.chess_id}, {self.player2.chess_id}, or 'draw'.")
        
        self.result = result
        self.completed = True

        if result == self.player1.chess_id:
            self.player1.points += 1
        elif result == self.player2.chess_id:
            self.player2.points += 1
        elif result == 'draw':
            self.player1.points += 0.5
            self.player2.points += 0.5

    def to_dict(self):
        winner = self.result
        return {
            'players': [self.player1.chess_id, self.player2.chess_id if self.player2 else None],
            'completed': self.completed,
            'winner': winner
        }
