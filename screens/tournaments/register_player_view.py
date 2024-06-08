from ..base_screen import BaseScreen
from models.player import Player
from commands import NoopCmd
import json
from pathlib import Path


class RegisterPlayerView(BaseScreen):
    def __init__(self, tournament, ongoing_tournaments, completed_tournaments):
        self.tournament = tournament
        self.ongoing_tournaments = ongoing_tournaments
        self.completed_tournaments = completed_tournaments
        self.players = self.load_players()

    def load_players(self, data_folder="data/clubs"):
        players = []
        data_folder_path = Path(data_folder)
        for filepath in data_folder_path.glob("*.json"):
            with open(filepath, 'r') as file:
                club_data = json.load(file)
                players.extend(club_data["players"])
        return players

    def display(self):
        print(f"Registering player for tournament: {self.tournament.name}")

        while True:
            print("\nOptions:")
            print("1. View all players")
            print("2. Search player by Chess ID")
            print("3. Search player by name")
            print("4. Register a new player")
            print("X. Return to manage tournament")
            choice = input("Select an option: ").strip().lower()

            if choice == '1':
                self.display_players(self.players)
            elif choice == '2':
                chess_id = input("Enter Chess ID: ").strip()
                results = self.search_player_by_id(chess_id)
                self.handle_search_results(results)
            elif choice == '3':
                name_fragment = input("Enter part of the player's name: ").strip()
                results = self.search_player_by_name(name_fragment)
                self.handle_search_results(results)
            elif choice == '4':
                self.register_new_player()
            elif choice == 'x':
                break
            else:
                print("Invalid option. Please try again.")

    def display_players(self, players):
        for index, player in enumerate(players, start=1):
            print(f"{index}. {player['name']} (ID: {player['chess_id']}) - {player['email']}")

    def search_player_by_id(self, chess_id):
        return [player for player in self.players if player['chess_id'] == chess_id]

    def search_player_by_name(self, name_fragment):
        name_fragment = name_fragment.lower()
        return [player for player in self.players if name_fragment in player['name'].lower()]

    def handle_search_results(self, results):
        if results:
            self.display_players(results)
            selection = input("Select a player by entering number 1 to register them or type X to cancel: ").strip()
            if selection.lower() == 'x':
                return
            try:
                if selection == "1":
                    player_index = int(selection) - 1
                    if player_index < 0 or player_index >= len(results):
                        raise ValueError
                    selected_player = results[player_index]
                    self.register_existing_player(selected_player)
            except ValueError:
                print("Invalid selection. Please try again.")
        else:
            print("No players found matching the search criteria.")

    def register_existing_player(self, player):
        new_player = Player(
            chess_id=player['chess_id'],
            name=player['name'],
            email=player['email'],
            birthday=player['birthday']
        )
        self.tournament.players.append(new_player)
        print(f"Player {player['name']} with ID {player['chess_id']} has been registered.")
        self.tournament.save()

    def register_new_player(self):
        chess_id = self.input_chess_id(prompt="Enter the player's chess ID")
        name = self.input_string(prompt="Enter the player's name", empty=True)
        email = self.input_email(prompt="Enter the player's email")
        birthday = self.input_birthday(prompt="Enter the player's birthday (dd-mm-yyyy)")

        new_player = Player(chess_id=chess_id, name=name, email=email, birthday=birthday)
        self.tournament.players.append(new_player)
        self.players.append({
            "name": name,
            "email": email,
            "chess_id": chess_id,
            "birthday": birthday
        })
        print(f"Player {name} with ID {chess_id} has been registered.")
        self.tournament.save()

    def get_command(self):
        return NoopCmd("tournament-players", tournament=self.tournament,
                       ongoing_tournaments=self.ongoing_tournaments, completed_tournaments=self.completed_tournaments)
