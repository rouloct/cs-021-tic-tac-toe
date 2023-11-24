"""
Rory Ulmer
CS 021 / Spring 2023
Tic-Tac-Toe

This is a simple Tic-Tac-Toe game. The user is able to play against the computer.
The computer is programmed to always play the best move, and will never lose the game.
"""

# Define Constants
COMPUTER = "Computer"
HUMAN = "Human"
EMPTY = "Empty"
TIE = "Tie"

PLAYERS = [HUMAN, COMPUTER]
SYMBOLS = {COMPUTER: "O", HUMAN: "X", EMPTY: "-"}
BOARD_SIZE = 9

HUMAN_WIN_RATING = -1
TIE_RATING = 0
COMPUTER_WIN_RATING = 1


# MAIN FUNCTION
def main():
    """ Begin program execution.
    Params - none
    Returns - none """

    # Display the game's introduction.
    display_intro()

    # Keep playing until the user decides to stop.
    play_again_strings = ["y", "Y", "yes", "Yes", "YES"]
    play_again = True

    while play_again:
        # Play the game and get the result.
        winner = play_game()

        # Display message based on the result.
        if winner == COMPUTER:
            print("Well, that was easy.")
        elif winner == HUMAN:
            print("Uh oh, that shouldn't have happened.")
        elif winner == TIE:
            print("Hey, you're not as bad as I thought.")

        # Prompt user to play again.
        print("Do you want to play again? (y/n)")
        play_again = input(">>> ") in play_again_strings

        if play_again:
            print("\nHere we go... ")

    # Display ending message when user decides to stop.
    display_ending()


# DISPLAY FUNCTIONS
def display_intro():
    """ Displays the intro to the game and waits for the user to play.
    Params - none
    Returns - none"""

    # Heading
    print("\n==================")
    print("RORY'S TIC-TAC-TOE")
    print("==================\n")

    # Introduction
    print("Welcome to RORY'S TIC-TAC-TOE!")
    print("So you think you're smarter than a computer?")
    print("Fine, I'll teach you how to play with me.\n")

    # Instructions
    print("Each square on the board has a corresponding number:")
    print(f"1 2 3")
    print(f"4 5 6")
    print(f"7 8 9")
    print("When prompted for a move, simply enter the number you want to place a piece on!\n")

    # Prompts user for input.
    print("Type 'y' to begin...")
    ready = input(">>> ")

    # Displays a message each time the user fails to enter a valid input that increase in agitation as
    # the user continues to not choose to start the game.
    times_failed = 0
    fail_messages = ["No problem, I'm patient.", "Trust me, I can wait.",
                     "Are you ready yet?", "Do you even want to play this game?",
                     "Okay, I'm already sick of you."]
    ready_strings = ["y", "Y", "yes", "Yes", "YES"]

    while ready not in ready_strings:
        if times_failed < len(fail_messages):
            print(f"{fail_messages[times_failed]} Type 'y' to begin...")
            times_failed += 1
        else:
            print("*ANGRY NOISES* Type 'y' to begin...")

        ready = input(">>> ")

    print("\nGreat job! You're ready to play! Here we go...")


def display_ending():
    """ Displays the ending message.
    Params - none
    Returns - none """

    print("\nThank you for playing RORY'S TIC-TAC-TOE!!!\n")
    print("Would you have stayed longer if I weren't so mean?")
    print("You know, it's not my fault I was made this way...")


def print_board(board):
    """ Displays the board.
    Params -
        board: [string]
    Returns - none """

    # Get the current player and winner (if there is one).
    current_player = get_current_player(board)
    winner = get_end_result(board)

    # Make a header for the board, depending on the current player or if the game is over.
    if winner == COMPUTER:
        header = f"{COMPUTER} Wins!"
    elif winner == HUMAN:
        header = f"{HUMAN} Wins!"
    elif winner == TIE:
        header = "Tie Game"
    else:
        header = f"{current_player}'s Turn"

    # Prints the board.
    print(f"\n{header}")
    print(f"{board[0]} {board[1]} {board[2]}")
    print(f"{board[3]} {board[4]} {board[5]}")
    print(f"{board[6]} {board[7]} {board[8]}\n")


# PLAY FUNCTIONS
def play_game():
    """ Plays the game until the game is over.
    Params - none
    Returns -
        result: string - the winner of the game."""

    # Initialize the board.
    board = get_new_board()

    # Initialize the turn counter.
    turn_counter = 1

    is_game_over = False
    while not is_game_over:
        # Play the game until the game is over.
        if turn_counter % 2 == 1:
            board = user_turn(board)
        else:
            board = computer_turn(board)

        is_game_over = get_end_result(board) is not None
        turn_counter += 1

    # Print the board one more time when the game is over.
    print_board(board)

    # Return the winner of the game (or a tie)
    return get_end_result(board)


def place_piece(board, target_square):
    """ Attempts to add a piece to the board. Does not modify the current board.
    Params -
        board: [string]
        target_square: int
    Returns -
        new_board: [string] """

    # Copy the current board.
    new_board = [] + board

    # Get the current player.
    current_player = get_current_player(new_board)

    # Error handling, but should never happen.
    # The game should not already be over.
    if get_end_result(new_board) is not None:
        print(f"Placement Error: Game already over.")
        return new_board

    # Target square should be between 1 and 9.
    if target_square > BOARD_SIZE or target_square < 0:
        print("Placement Error: Target square is invalid.")
        return new_board

    # Validate that the target square is empty.
    if new_board[target_square] != SYMBOLS[EMPTY]:
        print("Placement Error: Target square is not empty.")
        return new_board

    # Get the player's symbol.
    player_symbol = SYMBOLS[current_player]

    # Add the piece to the board.
    new_board[target_square] = player_symbol

    # Return the new board.
    return new_board


def user_turn(board):
    """ Gets the move from the user and plays the move.
    Params -
        board: [string]
    Returns -
        new_board: [string] """

    # Validate input.
    square = None
    while square is None:

        # Print the board.
        print_board(board)

        # Get user input.
        print("Enter a square...")
        try:
            target = int(input(">>> ")) - 1

        except ValueError:
            print("Please enter a valid number.")

        else:
            if target not in get_empty_squares(board):
                print("Error: Illegal move.")
            else:
                square = target

    # Play the move.
    new_board = place_piece(board, square)

    # Return the new board.
    return new_board


def computer_turn(board):
    """ Gets the computer's move and plays the move.
    Params -
        board: [string]
    Returns -
        new_board: [string] """

    # Print board and let the user know the computer might take a moment.
    print_board(board)
    print("I'm thinking...")

    # Get the computer's chosen move.
    square, _ = find_best_move(board)

    # Get the new board.
    new_board = place_piece(board, square)

    # Return the new board.
    return new_board


# ACCESSORY FUNCTIONS
def get_new_board():
    """ Return a new board.
    Params - none
    Returns -
        [string] """
    return [SYMBOLS[EMPTY]] * BOARD_SIZE


def get_empty_squares(board):
    """ Returns a list of all empty squares.
    Params -
        board: [string]
    Returns -
        empty_squares: [int] """

    return [index for index, square in enumerate(board) if square == SYMBOLS[EMPTY]]


def get_current_player(board):
    """ Returns the current player.
    Params -
        board: [string]
    Returns -
        current_player: string, one of HUMAN, COMPUTER, or None"""

    # If the game is a tie or already won, return None.
    if get_end_result(board) is not None:
        return None

    # Count how many pieces have been placed.
    pieces_placed = BOARD_SIZE - len(get_empty_squares(board))

    # If an even number of pieces have been placed, return the human.
    # If an odd number of pieces have been placed, return the computer.
    if pieces_placed % 2 == 0:
        return HUMAN
    else:
        return COMPUTER


def get_end_result(board):
    """ Returns the current result of the game (winner, tie, in-progress).
    Params -
        board: [string]
    Returns -
        winner: string, one of HUMAN, COMPUTER, TIE, or None"""

    # Define a list of all possible winning combinations of squares.
    winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                            (0, 3, 6), (1, 4, 7), (2, 5, 8),
                            (0, 4, 8), (2, 4, 6)]

    # Loop through both players (human and computer).
    for player in PLAYERS:

        # Get the player's symbol.
        player_symbol = SYMBOLS[player]

        # Checks each winning combination to see if the player has won. If so, returns True.
        for winning_combination in winning_combinations:
            if board[winning_combination[0]] == player_symbol \
                and board[winning_combination[1]] == player_symbol \
                    and board[winning_combination[2]] == player_symbol:
                return player

    # If the board is full and no player has won, the game is a tie.
    if len(get_empty_squares(board)) == 0:
        return TIE

    # If no player has won and no tie, return None.
    return None


# RECURSIVE FUNCTIONS
def find_best_move(board):
    """ Recursively finds the best move.
    Params -
        board: [string]
    Returns -
        square: int - the square of the next best move.
        rating: int - the rating of the current move.
    Explanation -
        This function will loop through all possible moves until the game is over.
        For each move that ends the game, it will return a rating of -1, 0, or 1 (human win, tie, computer win).
        Each move has 1-8 possible moves that can follow it that are stored in a list.
        Out of this list, the best move will be chosen by the most desired rating:
        The human would choose the move with the lowest rating, computer will choose the highest.
        After a move has found the best move, it returns itself and that rating...
        So each move "sets its own rating" as the most desired rating of the next possible moves.
        This recursively happens, with the best move being chosen at every step.
        When it gets back to the first move, it will have effectively "considered"  the best choice for future moves
        as well for both players. """

    # Get empty squares.
    empty_squares = get_empty_squares(board)

    # Check if the game is over. If so, return None, rating, where None is the square of the next best move
    # As the game is over and no more moves can be made.
    end_result = get_end_result(board)
    if end_result == HUMAN:
        return None, HUMAN_WIN_RATING
    elif end_result == TIE:
        return None, TIE_RATING
    elif end_result == COMPUTER:
        return None, COMPUTER_WIN_RATING

    # Initialize a list of moves.
    # Each move is a tuple of the target square and the rating.
    moves = []

    # Loop through all empty squares.
    for empty_square in empty_squares:

        # Get the new board with the piece placed at the empty square.
        new_board = place_piece(board, empty_square)

        # Recursively call the function.
        rating = find_best_move(new_board)[1]

        # Add the move to the list of moves.
        moves.append((empty_square, rating))

    # Get the current player.
    current_player = get_current_player(board)

    # The player will choose the move with the lowest rating
    # The computer will choose the move with the highest rating.
    if current_player == HUMAN:
        best_square, rating = min(moves, key=lambda m: m[1])
    else:
        best_square, rating = max(moves, key=lambda m: m[1])

    # Return the best square and its rating
    return best_square, rating


# PROGRAM START
if __name__ == "__main__":
    main()
