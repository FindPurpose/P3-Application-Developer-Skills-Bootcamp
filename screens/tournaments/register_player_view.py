from ..base_screen import BaseScreen
from models.player import Player
from commands import NoopCmd

class RegisterPlayerView(BaseScreen):
    def __init__(self, tournament):
        self.tournament = tournament

    def display(self):
        print(f"Registering player for tournament: {self.tournament.name}")
        chess_id = self.input_chess_id(prompt="Enter the player's chess ID")
        name = self.input_string(prompt="Enter the player's name", empty=True)
        email = self.input_email(prompt="Enter the player's email")
        birthday = self.input_birthday(prompt="Enter the player's birthday (dd-mm-yyyy)")

        new_player = Player(chess_id=chess_id, name=name, email=email, birthday=birthday)
        self.tournament.players.append(new_player)
        print(f"Player {name} with ID {chess_id} has been registered.")

        # Save the updated tournament
        self.tournament.save()

    def get_command(self):
        # After registering a player, return to the tournament players view
        return NoopCmd("tournament-players", tournament=self.tournament)
