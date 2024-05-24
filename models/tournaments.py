import json
from datetime import datetime
from pathlib import Path

class Tournament:
    def __init__(self, name, start_date, end_date, venue, number_of_rounds, filepath=None):
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
                "from": self.start_date.strftime("%d-%m-%Y"),
                "to": self.end_date.strftime("%d-%m-%Y"),
            },
            "venue": self.venue,
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "completed": self.completed,
            "players": self.players,
            "rounds": [[{
                "players": match.players,
                "completed": match.completed,
                "winner": match.winner
            } for match in round.matches] for round in self.rounds]
        }

        with open(self.filepath, 'w') as file:
            json.dump(data, file, indent=4)

"""
Get the tournament and put all of those into a placeholder.

import json
from .player import Player
from .round import Round
from .match import Match
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional
import random

class Tournament:
    def __init__(self, filepath=None, name=None):
        The constructor works in two ways:
        - if the filepath is provided, it loads data from JSON
        - if it is not but a name is provided, it creates a new tournament (and a new JSON file)
        
        self.name = name
        self.filepath = filepath
        self.start_date = None
        self.end_date = None
        self.venue = None
        self.number_of_rounds = None
        self.current_round = 0
        self.completed = False
        self.players = []
        self.rounds = []

        if filepath and not name:
            # Load data from the JSON file
            with open(filepath) as fp:
                data = json.load(fp)
                self.name = data["name"]
                self.start_date = datetime.strptime(data["dates"]["from"], "%d-%m-%Y")
                self.end_date = datetime.strptime(data["dates"]["to"], "%d-%m-%Y")
                self.venue = data["venue"]
                self.number_of_rounds = data["number_of_rounds"]
                self.current_round = data["current_round"]
                self.completed = data["completed"]
                self.players = [Player(chess_id) for chess_id in data["players"]]
                self.rounds = [
                    Round([Match(self.find_player_by_id(match["players"][0]), self.find_player_by_id(match["players"][1]), match["winner"]) for match in round])
                    for round in data["rounds"]
                ]
        elif not filepath and name:
            # We did not have a file, so we are going to create it by running the save method
            self.save()

    def find_player_by_id(self, chess_id):
        for player in self.players:
            if player.chess_id == chess_id:
                return player
        return None

    def create_first_round(self):
        random.shuffle(self.players)
        matches = [Match(self.players[i], self.players[i + 1]) for i in range(0, len(self.players), 2)]
        self.rounds.append(Round(matches))

    def create_next_round(self):
        sorted_players = sorted(self.players, key=lambda x: x.points, reverse=True)
        matches = []
        while sorted_players:
            player1 = sorted_players.pop(0)
            for i, player2 in enumerate(sorted_players):
                if not self.has_played_before(player1, player2):
                    matches.append(Match(player1, player2))
                    sorted_players.pop(i)
                    break
        self.rounds.append(Round(matches))

    def has_played_before(self, player1, player2):
        for round in self.rounds:
            for match in round.matches:
                if (match.player1 == player1 and match.player2 == player2) or (match.player1 == player2 and match.player2 == player1):
                    return True
        return False

    def save(self):
        Save the tournament data to a JSON file.
        data = {
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
                [{"players": [match.player1.chess_id, match.player2.chess_id], "completed": match.completed, "winner": match.result} for match in round.matches]
                for round in self.rounds
            ]
        }
        with open(f"data/tournaments/{self.name.replace(' ', '_')}.json", 'w') as fp:
            json.dump(data, fp, indent=4)
    
"""