from .base import BaseCommand
from commands.context import Context
from models.tournament_manager import TournamentManager
from .tournament_list import TournamentListCmd


class CreateTournamentCmd(BaseCommand):
    """Command to create a tournament"""

    def __init__(self, name, start_date, end_date, venue, number_of_rounds):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.venue = venue
        self.number_of_rounds = number_of_rounds

    def execute(self):
        """Uses a TournamentManager instance to create the tournament"""
        tm = TournamentManager()
        tm.create_tournament(
            self.name, 
            self.start_date, 
            self.end_date, 
            self.venue, 
            self.number_of_rounds
        )
        return Context("tournament-view", ongoing_tournaments=tm.ongoing_tournaments,
                       completed_tournaments=tm.completed_tournaments)
