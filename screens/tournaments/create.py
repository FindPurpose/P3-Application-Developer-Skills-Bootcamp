from datetime import datetime
from ..base_screen import BaseScreen
from commands.create_tournament import CreateTournamentCmd

class CreateNewTournament(BaseScreen):
    """Screen displayed when creating a tournament"""

    display = "## Create Tournament"

    def get_command(self):
        print("Creating a new tournament...")
        name = self.input_string("Enter tournament name: ")
        start_date_str = self.input_string("Enter start date (dd-mm-yyyy): ")
        end_date_str = self.input_string("Enter end date (dd-mm-yyyy): ")
        venue = self.input_string("Enter venue: ")
        
        while True:
            try:
                number_of_rounds = int(self.input_string("Enter number of rounds: "))
                break
            except ValueError:
                print("Invalid input. Please enter an integer for the number of rounds.")
        
        # Convert input strings to datetime objects
        start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
        end_date = datetime.strptime(end_date_str, "%d-%m-%Y")

        return CreateTournamentCmd(name, start_date, end_date, venue, number_of_rounds)