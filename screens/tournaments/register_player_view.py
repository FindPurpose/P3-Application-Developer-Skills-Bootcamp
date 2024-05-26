from ..base_screen import BaseScreen
from commands import NoopCmd, ExitCmd
from models.tournament_operations import TournamentOperations


class RegisterPlayerView(BaseScreen):
    def __init__(self, tournament, tournaments, players):
        self.tournament = tournament
        self.tournaments = tournaments
        self.players = players
        self.operations = TournamentOperations()

    def display(self):
        print("Available Players:")
        for player in self.players:
            print(f"ID: {player.id}, Name: {player.name}")

    def get_command(self):
        player_id = self.input_string("Enter the Chess Identifier of the player to register (or X to cancel): ").upper()
        if player_id == "X":
            return NoopCmd("tournament-players", tournament=self.tournament, tournaments=self.tournaments)
        for player in self.players:
            if player_id == player.id:
                self.operations.register_player(self.tournament, player_id)
                print(f"Player {player.name} registered.")
                return NoopCmd("tournament-players", tournament=self.tournament, tournaments=self.tournaments)
        print("Player not found.")
        return NoopCmd("register-player", tournament=self.tournament, tournaments=self.tournaments, players=self.players)
