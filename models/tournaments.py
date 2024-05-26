from datetime import datetime
from pathlib import Path
import json

class Tournament:
    def __init__(self, name, start_date, end_date, venue, number_of_rounds, filepath):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.venue = venue
        self.number_of_rounds = number_of_rounds
        self.current_round = None
        self.completed = False
        self.players = []
        self.rounds = []
        self.filepath = filepath

    def save(self):
        data = {
            "name": self.name,
            "dates": {
                "from": self.start_date.strftime('%d-%m-%Y'),
                "to": self.end_date.strftime('%d-%m-%Y'),
            },
            "venue": self.venue,
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "completed": self.completed,
            "players": self.players,
            "rounds": [
                [{"players": match.players, "completed": match.completed, "result": match.result} for match in round.matches]
                for round in self.rounds
            ]
        }
        with open(self.filepath, 'w') as file:
            json.dump(data, file, indent=4)
