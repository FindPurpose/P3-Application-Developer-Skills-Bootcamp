import json
from pathlib import Path
from datetime import datetime
from .tournaments import Tournament
from models import  Round, Match

class TournamentManager:
    def __init__(self, data_folder="data/tournaments"):
        datadir = Path(data_folder)
        self.data_folder = datadir
        self.tournaments = []
        for filepath in datadir.iterdir():
            if filepath.is_file() and filepath.suffix == ".json":
                try:
                    with open(filepath, 'r') as file:
                        data = json.load(file)
                        # Parse tournament data
                        tournament = Tournament(
                            name=data["name"],
                            start_date=datetime.strptime(data["dates"]["from"], "%d-%m-%Y"),
                            end_date=datetime.strptime(data["dates"]["to"], "%d-%m-%Y"),
                            venue=data["venue"],
                            number_of_rounds=data["number_of_rounds"],
                            filepath=filepath
                        )
                        tournament.current_round = data.get("current_round")
                        tournament.completed = data.get("completed", False)
                        tournament.players = data.get("players", [])

                        # Parse rounds and matches
                        tournament.rounds = []
                        for round_data in data["rounds"]:
                            matches = [Match(players=m["players"], completed=m["completed"], result=m.get("result")) for m in round_data]
                            round_obj = Round(matches=matches)
                            tournament.rounds.append(round_obj)

                        self.tournaments.append(tournament)
                except json.JSONDecodeError:
                    print(filepath, "is an invalid JSON file.")

    def create(self, name, start_date, end_date, venue, number_of_rounds):
        filepath = self.data_folder / (name.replace(" ", "_") + ".json")
        tournament = Tournament(name=name, start_date=start_date, end_date=end_date, venue=venue, number_of_rounds=number_of_rounds, filepath=filepath)
        tournament.save()

        self.tournaments.append(tournament)
        return tournament
