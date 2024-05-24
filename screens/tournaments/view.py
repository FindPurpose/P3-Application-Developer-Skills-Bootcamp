from ..base_screen import BaseScreen
from commands import NoopCmd,ExitCmd

class TournamentView(BaseScreen):
    """Tournament view screen"""

    def __init__(self, tournaments):
        self.tournaments = tournaments

    def display(self):
        if not self.tournaments:
            print("No ongoing tournaments.")
            return

        print("List of Ongoing Tournaments:")
        for idx, tournament in enumerate(self.tournaments, 1):
            print(f"{idx}. {tournament.name} ({tournament.start_date.strftime('%d-%m-%Y')} to {tournament.end_date.strftime('%d-%m-%Y')})")

    def get_command(self):
        if not self.tournaments:
            print("Press Enter to return to the main menu.")
            self.input_string()
            return NoopCmd("main-menu")

        print("Type a tournament number to view its players or X to return to the main menu.")
        value = self.input_string()
        if value.isdigit():
            value = int(value)
            if value in range(1, len(self.tournaments) + 1):
                return NoopCmd("tournament-players", tournament=self.tournaments[value - 1])
        elif value.upper() == "X":
            return NoopCmd("main-menu")
