from commands.context import Context
from models.tournament_manager import TournamentManager
from .base import BaseCommand

class TournamentListCmd(BaseCommand):
    """Command to get the list of tournaments"""

    def execute(self):
        tm = TournamentManager()
        return Context("tournament-view", tournaments=tm.tournaments)
