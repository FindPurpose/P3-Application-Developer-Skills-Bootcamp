from ..base_screen import BaseScreen
from commands import NoopCmd
from models.tournament_operations import TournamentOperations
from screens.tournaments.register_player_view import RegisterPlayerView


class TournamentPlayersView(BaseScreen):
    def __init__(self, tournament, ongoing_tournaments, completed_tournaments):
        self.tournament = tournament
        self.ongoing_tournaments = ongoing_tournaments
        self.completed_tournaments = completed_tournaments
        self.operations = TournamentOperations()

    def display(self):
        print(f"Tournament: {self.tournament.name}")
        print("Players:")
        for player_id in self.tournament.players:
            print(f" - {player_id}")

    def get_command(self):
        print("Options:")
        print("R - Register a player")
        print("E - Enter match results for current round")
        print("A - Advance to the next round")
        print("G - Generate tournament report")
        print("X - Return to tournaments list")
        value = self.input_string().upper()

        if value == "R":
            return RegisterPlayerView(self.tournament, self.ongoing_tournaments, self.completed_tournaments).run()
        elif value == "E":
            if self.tournament.current_round:
                round_number = self.tournament.current_round
                self.enter_match_results(round_number)
            else:
                print("No current round to enter results for.")
        elif value == "A":
            self.advance_to_next_round()
        elif value == "G":
            self.operations.generate_tournament_report(self.tournament)
        elif value == "X":
            return NoopCmd("tournament-view", ongoing_tournaments=self.ongoing_tournaments, completed_tournaments=self.completed_tournaments)
        return NoopCmd("tournament-players", tournament=self.tournament, ongoing_tournaments=self.ongoing_tournaments, completed_tournaments=self.completed_tournaments)

    def enter_match_results(self, round_number):
        round = self.tournament.rounds[round_number - 1]
        match_results = []
        for match in round.matches:
            result = self.input_string(f"Enter result for match {match.player1} vs {match.player2} (winner ID or 'D' for draw): ")
            match_results.append(result if result != 'D' else None)
        self.operations.enter_match_results(self.tournament, round_number, match_results)
        print("Match results entered.")

    def advance_to_next_round(self):
        confirmation = self.input_string("Are you sure you want to advance to the next round? (Y/N): ").upper()
        if confirmation == "Y":
            self.operations.advance_to_next_round(self.tournament)
            print("Advanced to the next round.")
