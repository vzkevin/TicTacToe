import math
import time
from player import HumanPlayer, SmartComputerPlayer


# Game board
class TicTacToe:
    def __init__(self):
        self.board = self.make_board()  # Initialize the game board
        self.current_winner = None  # Track the current winner

    @staticmethod
    def make_board():
        return [" " for _ in range(9)]  # Make a 3x3 game board

    def print_board(self):
        # Print the current state of the game board
        for row in [self.board[i * 3 : (i + 1) * 3] for i in range(3)]:
            print("| " + " | ".join(row) + " |")

    @staticmethod
    def print_board_nums():
        # Print the board numbers, to help users understand where to place their pieces
        number_board = [[str(i) for i in range(j * 3, (j + 1) * 3)] for j in range(3)]
        for row in number_board:
            print("| " + " | ".join(row) + " |")

    def make_move(self, square, letter):
        # Make a move; return True if successful
        if self.board[square] == " ":
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # Check for a winner in the current state of the game
        row_ind = math.floor(square / 3)
        row = self.board[row_ind * 3 : (row_ind + 1) * 3]
        if all([s == letter for s in row]):
            return True
        col_ind = square % 3
        column = [self.board[col_ind + i * 3] for i in range(3)]
        if all([s == letter for s in column]):
            return True
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([s == letter for s in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([s == letter for s in diagonal2]):
                return True
        return False

    def empty_squares(self):
        # Check if any empty squares
        return " " in self.board

    def num_empty_squares(self):
        # Count the number of empty squares
        return self.board.count(" ")

    def available_moves(self):
        # Return the indices of all available squares on the board
        return [i for i, x in enumerate(self.board) if x == " "]


def play(game, x_player, o_player, print_game=True):
    # This function runs the game loop, alternating between players and checking game status
    if print_game:
        game.print_board_nums()

    letter = "X"  # Start with the X player
    while game.empty_squares():
        if letter == "O":
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)
        if game.make_move(square, letter):
            if print_game:
                print(letter + " makes a move to square {}".format(square))
                game.print_board()
                print("")

            if game.current_winner:
                if print_game:
                    print(letter + " wins!")
                return letter  # ends the loop and exits the game
            letter = "O" if letter == "X" else "X"  # switches player

        time.sleep(0.8)  # Pause briefly to make the game flow better

    if print_game:
        print("It's a tie!")  # If the game ends in a tie, print a message


if __name__ == "__main__":
    x_player = SmartComputerPlayer(
        "X"
    )  # Initialize the X player (smart computer player)
    o_player = HumanPlayer("O")  # Initialize the O player (human player)
    t = TicTacToe()  # Start a new game
    play(t, x_player, o_player, print_game=True)  # Play the game
