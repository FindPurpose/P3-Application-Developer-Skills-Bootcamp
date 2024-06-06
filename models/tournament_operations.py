import json
import random
from pathlib import Path
from datetime import datetime
from models import Tournament, Round, Match, Player
from screens.tournaments.register_player_view import RegisterPlayerView

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
                match.set_result(match_results[i])  # Use set_result method to handle result setting and completed status

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
        report += f"Dates: {tournament.start_date.strftime('%Y-%m-%d')} to {tournament.end_date.strftime('%Y-%m-%d')}\n"
        report += f"Venue: {tournament.venue}\n"
        report += f"Number of Rounds: {tournament.number_of_rounds}\n"
        report += "Players:\n"
        
        sorted_players = sorted(tournament.players, key=lambda x: x.points, reverse=True)
        for player in sorted_players:
            report += f"  {player.name} (ID: {player.chess_id}) - {player.points} points\n"
        
        report += "Rounds:\n"
        for round_num, round in enumerate(tournament.rounds, 1):
            report += f"  Round {round_num}:\n"
            for match in round.matches:
                report += f"    Match: {match.player1.name} vs {match.player2.name if match.player2 else 'Bye'} - {'Completed' if match.completed else 'Incomplete'}\n"
                if match.result:
                    report += f"      Winner: {match.result if match.result else 'Draw'}\n"

        print(report)
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
            "players": [player.chess_id for player in tournament.players],
            "finished": tournament.completed,
            "rounds": [
                [
                    match.to_dict() for match in round.matches
                ]
                for round in tournament.rounds
            ]
        }

        with open(tournament.filepath, 'w') as file:
            json.dump(data, file, indent=4)
    
    def load(self, filepath):
        with open(filepath, 'r') as file:
            data = json.load(file)
        
        tournament = Tournament(
            name=data["name"],
            start_date=datetime.strptime(data["dates"]["from"], '%d-%m-%Y'),
            end_date=datetime.strptime(data["dates"]["to"], '%d-%m-%Y'),
            venue=data["venue"],
            number_of_rounds=data["number_of_rounds"],
        )
        tournament.current_round = data["current_round"]
        tournament.completed = data["completed"]
        tournament.players = [self.get_player_by_id(player_id) for player_id in data["players"]]
        tournament.rounds = [
            Round([self.create_match_from_dict(match_data) for match_data in round_data])
            for round_data in data["rounds"]
        ]
        
        return tournament
    

    def create_match_from_dict(self, match_data):
        player1 = RegisterPlayerView.search_player_by_id(match_data['players'][0])
        player2 = RegisterPlayerView.search_player_by_id(match_data['players'][1]) if match_data['players'][1] else None
        match = Match(player1, player2, match_data['completed'])
        match.result = match_data['winner']
        
        # Update player points based on the match result
        if match.result == player1.chess_id:
            match.set_result('player1')
        elif match.result == player2.chess_id:
            match.set_result('player2')
        elif match.result is None:
            match.set_result('draw')
        
        return match
    
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
