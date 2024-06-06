import json
from datetime import datetime
from pathlib import Path
from .player import Player
from .match import Match
from .round import Round
import os

class Tournament:
    def __init__(self, name, start_date, end_date, venue, number_of_rounds, filepath, players=None, rounds=None, current_round=0, completed=False):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.venue = venue
        self.number_of_rounds = number_of_rounds
        self.filepath = filepath
        self.players = players if players is not None else []
        self.rounds = rounds if rounds is not None else []
        self.current_round = current_round
        self.completed = completed
    
    def to_dict(self):
        return {
            "name": self.name,
            "dates": {
                "from": self.start_date.strftime("%d-%m-%Y"),
                "to": self.end_date.strftime("%d-%m-%Y")
            },
            "venue": self.venue,
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "completed": self.completed,
            "players": [player.chess_id for player in self.players],
            "rounds": [
                [
                    {
                        "players": [match.player1.chess_id, match.player2.chess_id],
                        "completed": match.completed,
                        "winner": match.result
                    }
                    for match in round.matches
                ]
                for round in self.rounds
            ]
        }
    
    @classmethod
    def from_dict(cls, data, filepath):
        players = [Player(**player_data) for player_data in data["players"]]
        rounds = []
        for round_data in data["rounds"]:
            matches = [
                Match(
                    player1=next(player for player in players if player.chess_id == m["players"][0]),
                    player2=next(player for player in players if player.chess_id == m["players"][1]),
                    completed=m["completed"],
                    result=m.get("winner")
                )
                for m in round_data
            ]
            rounds.append(Round(matches))
        start_date = datetime.strptime(data["dates"]["from"], "%d-%m-%Y")
        end_date = datetime.strptime(data["dates"]["to"], "%d-%m-%Y")
        return cls(
            name=data["name"],
            start_date=start_date,
            end_date=end_date,
            venue=data["venue"],
            number_of_rounds=data["number_of_rounds"],
            filepath=filepath,
            players=players,
            rounds=rounds,
            current_round=data["current_round"],
            completed=data["completed"]
        )
    
    def save(self):
        with open(self.filepath, 'r') as file:
            try:
                tournaments = json.load(file)
            except json.JSONDecodeError:
                tournaments = []

        # Ensure tournaments is a list of dictionaries
        if not isinstance(tournaments, list):
            tournaments = []

        # Update or append the tournament
        for i, tournament in enumerate(tournaments):
            if tournament['name'] == self.name:
                tournaments[i] = self.to_dict()
                break
        else:
            tournaments.append(self.to_dict())
        
        with open(self.filepath, 'w') as file:
            json.dump(tournaments, file, indent=4)
