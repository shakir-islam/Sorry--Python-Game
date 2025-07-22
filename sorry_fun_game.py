import random

def draw_card():
    """Draws a card from the deck."""
    #1-12 and sorry cards
    deck = [
        {"value": 1, "direction": "Moves the player one space."},
        {"value": 2, "direction": "Moves the player two spaces"},
        {"value": 3, "direction": "Move the player three spaces forward."},
        {"value": 4, "direction": "Move the player four spaces backward."},
        {"value": 5, "direction": "Move the player five spaces forward."},
        {"value": 7, "direction": "Move the player seven spaces forward, or split the seven spaces between two players."},
        {"value": 8, "direction": "Move the player eight spaces forward."},
        {"value": 10, "direction": "Move the player ten spaces forward."},
        {"value": 11, "direction": "Move the player spaces eleven forward."},
        {"value": 12, "direction": "Move the player to the start."},
        {"value": "Sorry!", "direction": "Move the player to another players spot, sending that player back to the Start."}
    ]
    return random.choice(deck)

def move(player_name, card, players, board_size):
    """Moves the current player based on the card drawn."""
    current_position = players[player_name]
    new_position = current_position
    value = card["value"]

    if current_position == "start":  #moves the player out of the start zone
        if value == 1 or value == 2 or value == "Sorry!":
            new_position = 1 if value == 1 else 2
            print(f"{player_name} moves out of Start Zone to position {new_position}.")
        else:
            print(f"{player_name} needs a '1', '2', or 'Sorry!' to leave the Start Zone!")
            return current_position

    #movement values/directions for each card
    elif value == 2:
        new_position += 2
    elif value == 3:
        new_position += 3
    elif value == 4:
        new_position -= 4
        if new_position < 0:
            new_position = 0
    elif value == 5:
        new_position += 5
    elif value == 7:
        while True:  #loops until a valid input is entered
            try:
                split_spaces = int(input(f"{player_name}, do you want to move one pawn 7 spaces or split the 7 spaces with the player infront? (Enter 1 or 2): "))
                if split_spaces == 1:
                    new_position += 7
                    break
                elif split_spaces == 2:
                    pawn1 = int(input(f"How many spaces? (0-7)"))
                    if 0 <= pawn1 <= 7:
                        pawn2 = 7 - pawn1
                        new_position += pawn1
                        for other_player, pos in players.items():
                            if other_player != player_name and pos == new_position:
                                players[other_player] = "start"
                                print(f"{player_name} landed on {other_player}'s spot! {other_player} goes back to the start!")
                        new_position += pawn2
                        break
                    else:
                        print("Invalid number of spaces. Please enter a value between 0 and 7.")
                else:
                    print("Invalid choice. Please enter '1' or '2'.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    elif value == 8:
        new_position += 8
    elif value == 10:
        new_position += 10
    elif value == 11:
        new_position += 11
    elif value == 12:
        new_position = 0
        print(f"{player_name} goes back to the start!")
    elif value == "Sorry!":
        chosen_player = input(f"Choose a player to send back to Start ({', '.join(p for p in players if p != player_name)}): ")
        while chosen_player not in players or chosen_player == player_name:
            print("Invalid choice. Please choose a valid player.")
            chosen_player = input(f"Choose a player to send back to Start ({', '.join(p for p in players if p != player_name)}): ")
        new_position = players[chosen_player]
        players[chosen_player] = "start"
        print(f"{player_name} took {chosen_player}'s spot, sending them back to Start!")

    if isinstance(new_position, int):  # uses isinstance(not learned in class) to make sure the position is within bounds
        if new_position < 0:
            new_position = 0
        elif new_position > board_size:
            print(f"{player_name} must draw exactly {board_size - current_position} to finish!")
            return current_position

        if new_position < board_size - 4:
            for other_player, pos in players.items():
                if other_player != player_name and pos == new_position:
                    players[other_player] = "start"
                    print(f"{player_name} landed on {other_player}'s spot! Sending them back to Start!")

    return new_position

def save(players):
    """Save the game state to a file."""
    with open("save_file.txt", "w") as myFile:
        for player, position in players.items():
            myFile.write(f"{player},{position}\n")
    print("Game saved!")

def load():
    """Load the game state from a file."""
    try:
        with open("save_file.txt", "r") as file:
            players = {}
            for line in file:
                name, position = line.strip().split(",")
                if position == 'start':
                    position = 0
                players[name] = int(position)
            print("Game loaded!")
            return players
    except FileNotFoundError:
        print("No game found. Starting a new game.")
        return None

def board(players, board_size):
    """Displays the board with each player's positions."""
    print("\n" + "==" * (board_size + 9))
    for position in range(board_size + 1):
        player_position = [name[0] for name, pos in players.items() if pos == position]
        marker = (
            "S" if position == 0 else
            "Z" if position >= board_size - 4 else
            "".join(player_position) if player_position else "-"
        )
        print(f"{marker:^3}", end="")
    print(f"\n{'==' * (board_size + 9)}")

def menu():
    """Display the main menu."""
    while True:  #makes sure one of the 5 options is chosen
        print("\nMain Menu:")
        print("1. Play Turn")
        print("2. Display Instructions")
        print("3. Display Board")
        print("4. Save Game")
        print("5. Quit")
        
        try:
            choice = int(input("Choose an option: "))
            if 1 <= choice <= 5: #handles any errors that could occur if the one of the options arent chosen
                return choice
            else:
                print("Please choose a valid option (1-5).")
        except ValueError:
            print("Invalid input! Please enter a number between 1 and 5.")

def rules():
    """Display the game rules."""
    print("""
    Sorry! Rules:
    1. Players start in the Start Zone (S) and must draw a '1', '2', or 'Sorry!' to enter the board.
    2. Draw cards to determine movement, swaps, or direction.
    3. Landing on another player sends them back to Start unless they are in the Safe Zone.
    4. Use the 'Sorry!' card to take another player's spot and send them back to Start.
    5. Exact card value is required to reach the finish line.
    6. First player to the end wins!
""")

def play_game():
    """Main game."""
    print("Welcome to Sorry!")

    players = load()  # loads a save file
    if not players:  # if no save game, sets up a new game with new players

        while True:
            try:
                num_players = int(input("Enter the number of players (2-4): "))
                if 2 <= num_players <= 4:
                    break
                else:
                    print("Please enter a valid number of players (2-4).")
            except ValueError:
                print("Invalid. Please enter a number.")

        players = {}
        for i in range(num_players):
            while True:
                player_name = input(f"Enter name for Player {i + 1}: ").strip()
                if player_name:
                    if player_name not in players:
                        players[player_name] = "start"
                        break
                    else:
                        print("Player name must be unique. Please enter a different name.")
                else:
                    print("Name cannot be empty. Please enter a valid name.")

    board_size = 50
    game_over = False

    while not game_over:
        option = menu()  # shows the menu

        if option == 1:
            for player_name in players.keys():
                print(f"\n{player_name}'s turn. Press Enter/return (if on mac) to draw a card.")
                input()  # waits for user to press enter/return

                card = draw_card()  # draws a card for the certain player
                print(f"{player_name} drew: {card['value']}")

                players[player_name] = move(player_name, card, players, board_size)  # moves the player

                board(players, board_size)

                if players[player_name] == board_size:  # checks for any winners
                    print(f"{player_name} wins!")
                    game_over = True
                    break

        elif option == 2:
            rules()

        elif option == 3:
            board(players, board_size)

        elif option == 4:
            print("Saving game...")
            save(players)  # saves the current game into the text file save_file.txt

        elif option == 5:
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    play_game()
