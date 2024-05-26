import json
from pathlib import Path
from datetime import datetime
from models import Tournament, Round, Match

class TournamentOperations:
    def __init__(self, data_folder="data/tournaments"):
        self.data_folder = Path(data_folder)

    def register_player(self, tournament, player_id):
        if player_id not in tournament.players:
            tournament.players.append(player_id)
            self.save(tournament)

    def enter_match_results(self, tournament, round_number, match_results):
        if round_number > len(tournament.rounds) or round_number < 1:
            print("Invalid round number.")
            return

        round = tournament.rounds[round_number - 1]
        for i, match in enumerate(round.matches):
            if match_results[i] is not None:
                match.completed = True
                match.winner = match_results[i]

        self.save(tournament)

    def advance_to_next_round(self, tournament):
        if tournament.current_round is None:
            tournament.current_round = 1
        elif tournament.current_round < tournament.number_of_rounds:
            tournament.current_round += 1
        else:
            tournament.completed = True

        self.save(tournament)

    def generate_tournament_report(self, tournament):
        report = f"Tournament Report: {tournament.name}\n"
        report += f"Dates: {tournament.start_date.strftime('%d-%m-%Y')} to {tournament.end_date.strftime('%d-%m-%Y')}\n"
        report += f"Venue: {tournament.venue}\n"
        report += f"Number of Rounds: {tournament.number_of_rounds}\n"
        report += "Rounds:\n"
        for round_num, round in enumerate(tournament.rounds, 1):
            report += f"  Round {round_num}:\n"
            for match in round.matches:
                report += f"    Match: {match.players} - {'Completed' if match.completed else 'Incomplete'}\n"

        return report

    def save(self, tournament):
        data = {
            "name": tournament.name,
            "dates": {
                "from": tournament.start_date.strftime('%d-%m-%Y'),
                "to": tournament.end_date.strftime('%d-%m-%Y'),
            },
            "venue": tournament.venue,
            "number_of_rounds": tournament.number_of_rounds,
            "current_round": tournament.current_round,
            "completed": tournament.completed,
            "players": tournament.players,
            "rounds": [
                [{"players": match.players, "completed": match.completed, "result": match.result} for match in round.matches]
                for round in tournament.rounds
            ]
        }
        with open(tournament.filepath, 'w') as file:
            json.dump(data, file, indent=4)
