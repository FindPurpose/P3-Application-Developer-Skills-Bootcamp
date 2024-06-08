from ..base_screen import BaseScreen
from commands import NoopCmd, ClubListCmd


class TournamentView(BaseScreen):
    def __init__(self, ongoing_tournaments, completed_tournaments):
        self.ongoing_tournaments = ongoing_tournaments
        self.completed_tournaments = completed_tournaments

    def display(self):
        print("List of Ongoing Tournaments:")
        for idx, tournament in enumerate(self.ongoing_tournaments, 1):
            start_date = tournament.start_date.strftime('%d-%m-%Y')
            end_date = tournament.end_date.strftime('%d-%m-%Y')
            print(f"{idx}. {tournament.name} ({start_date} to {end_date})")

        print("\nList of Completed Tournaments:")
        for idx, tournament in enumerate(self.completed_tournaments, 1):
            start_date = tournament.start_date.strftime('%d-%m-%Y')
            end_date = tournament.end_date.strftime('%d-%m-%Y')
            total_ongoing = len(self.ongoing_tournaments)
            print(f"{idx + total_ongoing}. {tournament.name} ({start_date} to {end_date})")

    def get_command(self):
        value = self.input_string("Type a tournament number to view its players or X to return.").upper()
        if value.isdigit():
            value = int(value)
            if value in range(1, len(self.ongoing_tournaments) + 1):
                return NoopCmd("tournament-players",
                               tournament=self.ongoing_tournaments[value - 1],
                               ongoing_tournaments=self.ongoing_tournaments,
                               completed_tournaments=self.completed_tournaments)
            elif value in range(len(self.ongoing_tournaments) + 1,
                                len(self.ongoing_tournaments) + len(self.completed_tournaments) + 1):
                return NoopCmd("tournament-players",
                               tournament=self.completed_tournaments[value - len(self.ongoing_tournaments) - 1],
                               ongoing_tournaments=self.ongoing_tournaments,
                               completed_tournaments=self.completed_tournaments)
        elif value == "X":
            return ClubListCmd()
        return NoopCmd("tournament-view",
                       ongoing_tournaments=self.ongoing_tournaments,
                       completed_tournaments=self.completed_tournaments)
