from random import choice
from player import Player


class Autoplayer(Player):
    def __init__(self, size=4):
        super().__init__(size=size)

    def choose_move(self, board):
        best_score, best_direction = float('-inf'), choice(self.directions)
        for direction in self.directions:
            move_score = self.test_move(board, direction)
            if move_score > best_score:
                best_score, best_direction = move_score, direction
        return best_direction

    def test_move(self, board, direction):
        test_board = board.clone()
        merges = test_board.move(direction)
        if merges != -1:
            return self.score_move(test_board.board, merges)
        return float('-inf')

    def score_move(self, board, merges):
        # After a move has been performed score it based on the board status
        smoothness = self.get_smoothness(board)
        empty_tiles = sum(x.count(0) for x in board)
        discordances = self.get_discordances(board)
        move_score = 0
        for var, multiplier in zip((smoothness, empty_tiles, merges, discordances),
                                   (-0.7, 0.75, 0.8, -0.6)):
            move_score += var * multiplier
        return move_score

    def get_smoothness(self, board):
        # AI should minimise the difference in value between adjacent tiles by row and column
        smoothness = 0
        for i in range(self.size):
            smoothness += self.get_variation([row[i] for row in board]) + self.get_variation(board[i])
        return smoothness

    def get_variation(self, arr):
        variation = 0
        for m, n in zip(arr, arr[1:]):  # pairwise subtraction
            variation += abs(m - n)
        return variation

    def get_discordances(self, board):
        """
        At a given stage in the game, a preferred sequence of tiles is something like: 32, 64, 128, 256
        A discordance is therefore something of the form 32, 2, 128, 256 which breaks the pattern
        The AI should aim to keep discordances at a minimum for both rows and columns
        """
        discordances = 0
        for i in range(self.size):
            row = board[i]
            if sorted(row) != row and sorted(row, reverse=True) != row:
                discordances += 1
            column = [row[i] for row in board]
            if sorted(column) != column and sorted(column, reverse=True) != column:
                discordances += 1
        return discordances
