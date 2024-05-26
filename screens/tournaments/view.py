from ..base_screen import BaseScreen
from commands import NoopCmd, ExitCmd

class TournamentView(BaseScreen):
    def __init__(self, ongoing_tournaments, completed_tournaments):
        self.ongoing_tournaments = ongoing_tournaments
        self.completed_tournaments = completed_tournaments

    def display(self):
        print("List of Ongoing Tournaments:")
        for idx, tournament in enumerate(self.ongoing_tournaments, 1):
            print(f"{idx}. {tournament.name} ({tournament.start_date.strftime('%d-%m-%Y')} to {tournament.end_date.strftime('%d-%m-%Y')})")
        print("\nList of Completed Tournaments:")
        for idx, tournament in enumerate(self.completed_tournaments, 1):
            print(f"{idx + len(self.ongoing_tournaments)}. {tournament.name} ({tournament.start_date.strftime('%d-%m-%Y')} to {tournament.end_date.strftime('%d-%m-%Y')})")

    def get_command(self):
        value = self.input_string("Type a tournament number to view its players or X to return to the main menu.").upper()
        if value.isdigit():
            value = int(value)
            if value in range(1, len(self.ongoing_tournaments) + 1):
                return NoopCmd("tournament-players", tournament=self.ongoing_tournaments[value - 1], ongoing_tournaments=self.ongoing_tournaments, completed_tournaments=self.completed_tournaments)
            elif value in range(len(self.ongoing_tournaments) + 1, len(self.ongoing_tournaments) + len(self.completed_tournaments) + 1):
                return NoopCmd("tournament-players", tournament=self.completed_tournaments[value - len(self.ongoing_tournaments) - 1], ongoing_tournaments=self.ongoing_tournaments, completed_tournaments=self.completed_tournaments)
        elif value == "X":
            return NoopCmd("main-menu")
        return NoopCmd("tournament-view", ongoing_tournaments=self.ongoing_tournaments, completed_tournaments=self.completed_tournaments)
