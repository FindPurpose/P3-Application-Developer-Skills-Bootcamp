# File: models/match.py
class Match:
    def __init__(self, player1, player2, completed=False, result=None):
        self.player1 = player1
        self.player2 = player2
        self.completed = completed
        self.result = result
    
    def set_result(self, result):
        if result not in ('player1', 'player2', 'draw'):
            raise ValueError("Result must be 'player1', 'player2', or 'draw'.")
        
        self.result = result
        self.completed = True
        
        if result == 'player1':
            self.player1.points += 1
            self.player2.points += 0
        elif result == 'player2':
            self.player1.points += 0
            self.player2.points += 1
        elif result == 'draw':
            self.player1.points += 0.5
            self.player2.points += 0.5

    def to_dict(self):
        return {
            'player1': self.player1.to_dict(),
            'player2': self.player2.to_dict(),
            'completed': self.completed,
            'result': self.result
        }
