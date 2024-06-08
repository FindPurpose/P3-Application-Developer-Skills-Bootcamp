from faker import Faker
from faker.providers import BaseProvider


class TournamentPlayerFaker:
    def __init__(self):
        self.fake = Faker()

    def generate_fake_player(self, chess_id):
        player_data = {
            "name": self.fake.name(),
            "email": self.fake.email(),
            "chess_id": chess_id,
            "birthday": self.fake.date_of_birth(minimum_age=18, maximum_age=65).strftime("%d-%m-%Y")
        }
        return player_data
