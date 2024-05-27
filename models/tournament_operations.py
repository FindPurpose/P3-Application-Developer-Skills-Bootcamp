import json
import random
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
            self.generate_first_round_pairings(tournament)
        elif tournament.current_round < tournament.number_of_rounds:
            self.generate_subsequent_round_pairings(tournament)
        else:
            tournament.completed = True
            self.save(tournament)
            print("Tournament has completed.")

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

    def generate_first_round_pairings(self, tournament):
        players = tournament.players[:]
        random.shuffle(players)
        matches = []
        for i in range(0, len(players), 2):
            if i + 1 < len(players):
                matches.append(Match(players[i], players[i + 1]))
            else:
                matches.append(Match(players[i], None))  # Handle odd number of players
        first_round = Round(matches)
        tournament.rounds.append(first_round)
        tournament.current_round = 1
        self.save(tournament)
    
    def generate_subsequent_round_pairings(self, tournament):
        players = sorted(tournament.players, key=lambda x: x.points, reverse=True)
        matches = []
        i = 0
        while i < len(players) - 1:
            match = (players[i], players[i + 1])
            if not self.has_played_before(tournament, match):
                matches.append(Match(*match))
                i += 2
            else:
                random.shuffle(players)
                i = 0
        new_round = Round(matches)
        tournament.rounds.append(new_round)
        tournament.current_round += 1
        self.save(tournament)
    
    def has_played_before(self, tournament, match):
        player1, player2 = match
        for round in tournament.rounds:
            for match in round.matches:
                if (match.player1 == player1 and match.player2 == player2) or (match.player1 == player2 and match.player2 == player1):
                    return True
        return False

