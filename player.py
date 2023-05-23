# This is the base Player class. It is an abstract class that should not be instantiated directly.
# The class is extended for different types of players
class Player:
    def __init__(self, letter):
        # "X" or "O"
        self.letter = letter

    # return the move that the player wants to make.
    def get_move(self, game):
        pass


# This class represents a human player.
class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)  # Call the init method of the parent class.

    # This function gets the move from the human player
    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + "'s turn. Input move (0-9): ")
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print("Invalid square. Try again.")
        return val


# This class represents a smart computer player that uses the minimax algorithm to determine the best move.
class SmartComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    # Gets the best move to make using the minimax algorithm.
    def get_move(self, game):
        # If this is the first move, choose a random position.
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())
        else:
            # Otherwise, use the minimax algorithm to find the best move.
            square = self.minimax(game, self.letter)["position"]
        return square

    # Implementation of the minimax algorithm. It finds the optimal move by simulating all possible games from the current state kinda like a tree of possibilitys, and returns the move that leads to the best possible outcome.
    def minimax(self, state, player):
        max_player = self.letter  # yourself
        other_player = "O" if player == "X" else "X"

        # First check if the previous move won the game.
        if state.current_winner == other_player:
            return {
                "position": None,
                # If the other player won, score is based on how many squares are left:
                # positive if the other player is us, negative if the other player is them.
                "score": 1 * (state.num_empty_squares() + 1)
                if other_player == max_player
                else -1 * (state.num_empty_squares() + 1),
            }
        # If the game has ended in a tie, return a score of 0.
        elif not state.empty_squares():
            return {"position": None, "score": 0}

        # Now start simulating games. If we are maximizing player, we want to maximize the score;
        # if we are the minimizing player, we want to minimize the score.
        if player == max_player:
            best = {
                "position": None,
                "score": -math.inf,
            }
        # each score should maximize (start with the lowest possible score)
        else:
            best = {
                "position": None,
                "score": math.inf,
            }
        # each score should minimize (start with the highest possible score)
        for possible_move in state.available_moves():
            # Try making the move and see what the score would be.
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player)
            # simulate a game after making that move

            # After simulating, undo the move.
            state.board[possible_move] = " "
            state.current_winner = None
            sim_score[
                "position"
            ] = possible_move  # this represents the move optimal next move

            # Update best score if this move is better.
            if player == max_player:
                if sim_score["score"] > best["score"]:
                    best = sim_score
            else:
                if sim_score["score"] < best["score"]:
                    best = sim_score
        return best
