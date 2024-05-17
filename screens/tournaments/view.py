from commands import ClubListCmd, NoopCmd

from ..base_screen import BaseScreen
from models import Tournament 


class TournamentView(BaseScreen):
    """Screen displayed when viewing a club"""

    def __init__(self, tournament):
        self.tournament = tournament

    def display_tournament_info(tournament: Tournament):
        print(f"Tournament: {tournament.name}")
        print(f"Dates: {tournament.start_date.strftime('%d-%m-%Y')} to {tournament.end_date.strftime('%d-%m-%Y')}")
        print(f"Venue: {tournament.venue}")
        print(f"Rounds: {tournament.number_of_rounds}")
        print(f"Current Round: {tournament.current_round if tournament.current_round else 'None'}")
        print(f"Completed: {'Yes' if tournament.completed else 'No'}")
        print("Players:")
        for player_id in tournament.players:
            print(f" - {player_id}")

    def get_command(self):
        """Gets the command for this screen"""
        while True:
            print("Select a player to view/edit it, or 'C' to create a new player.")
            print("Type 'B' to go back to main menu.")
            value = self.input_string()
            if value.upper() == "B":
                return ClubListCmd()
            elif value.upper() == "C":
                return NoopCmd("player-create", club=self.club)
            elif value.isdigit():
                value = int(value)
                return NoopCmd(
                    "player-view", club=self.club, player=self.club.players[value - 1]
                )

"""def display_tournament_info(tournament: Tournament):
        print(f"Tournament: {tournament.name}")
        print(f"Dates: {tournament.start_date.strftime('%d-%m-%Y')} to {tournament.end_date.strftime('%d-%m-%Y')}")
        print(f"Venue: {tournament.venue}")
        print(f"Rounds: {tournament.number_of_rounds}")
        print(f"Current Round: {tournament.current_round if tournament.current_round else 'None'}")
        print(f"Completed: {'Yes' if tournament.completed else 'No'}")
        print("Players:")
        for player_id in tournament.players:
            print(f" - {player_id}")

    def enter_match_results(tournament: Tournament, round_number: int, match_results: List[Optional[str]]):
        if round_number > len(tournament.rounds) or round_number < 1:
            print("Invalid round number.")
            return
    
        round = tournament.rounds[round_number - 1]
        for i, match in enumerate(round.matches):
            if match_results[i] is not None:
                match.completed = True
                match.winner = match_results[i]
    
        save(tournament, Path(f"data/tournaments/{tournament.name.replace(' ', '_')}.json"))

    def advance_to_next_round(tournament: Tournament):
        if tournament.current_round is None:
            tournament.current_round = 1
        elif tournament.current_round < tournament.number_of_rounds:
            tournament.current_round += 1
        else:
            tournament.completed = True
    
        save(tournament, Path(f"data/tournaments/{tournament.name.replace(' ', '_')}.json"))

    def generate_tournament_report(tournament: Tournament):
        report = f"Tournament Report: {tournament.name}\n"
        report += f"Dates: {tournament.start_date.strftime('%d-%m-%Y')} to {tournament.end_date.strftime('%d-%m-%Y')}\n"
        report += f"Venue: {tournament.venue}\n"
        report += "Players:\n"
        for player_id in tournament.players:
            report += f" - {player_id}\n"
        report += "Rounds:\n"
        for i, round in enumerate(tournament.rounds):
            report += f"  Round {i+1}:\n"
            for match in round.matches:
                report += f"    {match.players[0]} vs {match.players[1]} - "
                if match.completed:
                    report += f"Winner: {match.winner if match.winner else 'Draw'}\n"
                else:
                    report += "Not Completed\n"
        print(report)"""