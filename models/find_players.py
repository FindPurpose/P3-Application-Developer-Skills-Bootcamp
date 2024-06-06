import json
from pathlib import Path


def load_players(data_folder="data/clubs"):
    players = []
    data_folder_path = Path(data_folder)
    for filepath in data_folder_path.glob("*.json"):
        with open(filepath, 'r') as file:
            club_data = json.load(file)
            players.extend(club_data["players"])
    return players

def display_players(players):
    for index, player in enumerate(players, start=1):
        print(f"{index}. {player['name']} (ID: {player['chess_id']}) - {player['email']}")

def search_player_by_id(players, chess_id):
    return [player for player in players if player['chess_id'] == chess_id]

def search_player_by_name(players, name_fragment):
    name_fragment = name_fragment.lower()
    return [player for player in players if name_fragment in player['name'].lower()]

def select_and_register_player(players, tournament):
    display_players(players)
    selection = input("Select a player by number to register them or type X to cancel: ").strip()
    if selection.lower() == 'x':
        return
    try:
        player_index = int(selection) - 1
        if player_index < 0 or player_index >= len(players):
            raise ValueError
        selected_player = players[player_index]
        tournament['players'].append(selected_player['chess_id'])
        print(f"Player {selected_player['name']} has been registered for the tournament.")
    except ValueError:
        print("Invalid selection. Please try again.")


def register_player_for_tournament(tournament):
    players = load_players()
    while True:
        print("\nOptions:")
        print("1. View all players")
        print("2. Search player by Chess ID")
        print("3. Search player by name")
        print("X. Return to manage tournament")
        choice = input("Select an option: ").strip().lower()

        if choice == '1':
            display_players(players)
        elif choice == '2':
            chess_id = input("Enter Chess ID: ").strip()
            results = search_player_by_id(players, chess_id)
            if results:
                select_and_register_player(results, tournament)
            else:
                print("No player found with the given Chess ID.")
        elif choice == '3':
            name_fragment = input("Enter part of the player's name: ").strip()
            results = search_player_by_name(players, name_fragment)
            if results:
                select_and_register_player(results, tournament)
            else:
                print("No players found matching the given name fragment.")
        elif choice == 'x':
            break
        else:
            print("Invalid option. Please try again.")
