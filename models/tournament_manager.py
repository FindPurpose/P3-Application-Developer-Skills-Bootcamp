import json
from pathlib import Path
from datetime import datetime
from .tournaments import Tournament
from models import Round, Match
from .player import Player
from datetime import datetime


class TournamentManager:
    def __init__(self, data_folder="data/tournaments"):
        self.data_folder = Path(data_folder)
        self.ongoing_tournaments = []
        self.completed_tournaments = []
        self.load_tournaments()
    
    def load_tournaments(self):
        for filepath in self.data_folder.iterdir():
            if filepath.is_file() and filepath.suffix == ".json":
                with open(filepath, 'r') as file:
                    data = json.load(file)
                    print(f"Loaded data from {filepath}: {data}")  # Add this line to inspect the loaded data
                    players = [self.load_player(player_id) for player_id in data["players"]]
                    rounds = []
                    for round_data in data["rounds"]:
                        matches = [
                            Match(
                                player1=next(player for player in players if player.chess_id == m["players"][0]),
                                player2=next(player for player in players if player.chess_id == m["players"][1]),
                                completed=m["completed"],
                                result=m.get("result")
                            )
                            for m in round_data
                        ]
                        rounds.append(Round(matches))
                    start_date = datetime.strptime(data["dates"]["from"], "%d-%m-%Y")
                    end_date = datetime.strptime(data["dates"]["to"], "%d-%m-%Y")
                    tournament = Tournament(
                        name=data["name"],
                        start_date=start_date,
                        end_date=end_date,
                        venue=data["venue"],
                        number_of_rounds=data["number_of_rounds"],
                        players=players,
                        rounds=rounds,
                        current_round=data["current_round"],
                        completed=data["completed"],
                        filepath=filepath
                    )
                    if tournament.completed:
                        self.completed_tournaments.append(tournament)
                    else:
                        self.ongoing_tournaments.append(tournament)
    
    def load_player(self, player_id):
        # Dummy values for email and birthday
        return Player(chess_id=player_id, name=f"Player {player_id}", email=f"{player_id}@example.com", birthday="01-01-2000")
    
    def save_tournament(self, tournament):
        with open(tournament.filepath, 'w') as file:
            json.dump(tournament.to_dict(), file, indent=4)

    def create_tournament(self, name, start_date, end_date, venue, number_of_rounds):
        filepath = self.data_folder / f"{name.replace(' ', '_').lower()}.json"
        new_tournament = Tournament(name, start_date, end_date, venue, number_of_rounds, filepath)
        self.ongoing_tournaments.append(new_tournament)
        self.save_tournament(new_tournament)
        return new_tournament
