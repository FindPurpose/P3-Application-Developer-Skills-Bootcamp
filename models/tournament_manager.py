import json
from pathlib import Path
from datetime import datetime
from models import Tournament, Round, Match, Player
from .make_tournament import TournamentPlayerFaker

class TournamentManager:
    def __init__(self, data_folder="data/tournaments", player_data_folder="data/clubs"):
        self.data_folder = Path(data_folder)
        self.player_data_folder = Path(player_data_folder)
        self.players = self.load_players()
        self.ongoing_tournaments = []
        self.completed_tournaments = []
        self.player_faker = TournamentPlayerFaker()
        self.load_tournaments()

    def load_players(self):
        players = []
        for filepath in self.player_data_folder.glob("*.json"):
            with open(filepath, 'r') as file:
                club_data = json.load(file)
                for player_data in club_data["players"]:
                    player = Player(
                        name=player_data['name'],
                        email=player_data['email'],
                        chess_id=player_data['chess_id'],
                        birthday=player_data['birthday']
                    )
                    players.append(player)
        return players

    def load_tournaments(self):
        for filepath in self.data_folder.iterdir():
            if filepath.is_file() and filepath.suffix == ".json":
                with open(filepath, 'r') as file:
                    data = json.load(file)
                    print(f"Loaded data from {filepath}: {data}")
                    players = [self.get_or_create_player(player_id) for player_id in data["players"]]
                    rounds = []
                    for round_data in data["rounds"]:
                        matches = [
                            Match(
                                player1=self.get_or_create_player(m["players"][0]),
                                player2=self.get_or_create_player(m["players"][1]) if m["players"][1] else None,
                                completed=m["completed"],
                                result=m.get("winner")
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
                    self.recalculate_points(tournament)
                    if tournament.completed:
                        self.completed_tournaments.append(tournament)
                    else:
                        self.ongoing_tournaments.append(tournament)

    def recalculate_points(self, tournament):
        for round in tournament.rounds:
            for match in round.matches:
                if match.completed and match.result:
                    self.update_points(match, match.result)

    def get_player_by_id(self, player_id):
        return next((player for player in self.players if player.chess_id == player_id), None)

    def get_or_create_player(self, player_id):
        player = self.get_player_by_id(player_id)
        if player is None:
            fake_player_data = self.player_faker.generate_fake_player(player_id)
            player = Player(
                name=fake_player_data['name'],
                email=fake_player_data['email'],
                chess_id=fake_player_data['chess_id'],
                birthday=fake_player_data['birthday']
            )
            self.players.append(player)
        return player

    def update_points(self, match, result):
        if result == 'D':
            # Draw case
            if match.player1 and match.player2:
                match.player1.points += 0.5
                match.player2.points += 0.5
        else:
            # Winner case
            winner = self.get_player_by_id(result)
            if winner == match.player1:
                match.player1.points += 1
            elif winner == match.player2:
                match.player2.points += 1

    def save_tournament(self, tournament):
        with open(tournament.filepath, 'w') as file:
            json.dump(tournament.to_dict(), file, indent=4)

    def create_tournament(self, name, start_date, end_date, venue, number_of_rounds):
        filepath = self.data_folder / f"{name.replace(' ', '_').lower()}.json"
        new_tournament = Tournament(
            name=name,
            start_date=start_date,
            end_date=end_date,
            venue=venue,
            number_of_rounds=number_of_rounds,
            players=[],  # No players initially
            rounds=[],   # No rounds initially
            current_round=0,
            completed=False,
            filepath=filepath
        )
        self.ongoing_tournaments.append(new_tournament)
        self.save_tournament(new_tournament)
        return new_tournament
