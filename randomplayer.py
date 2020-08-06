from random import choice
from player import Player


class RandomPlayer(Player):
    def __init__(self, size=4):
        super().__init__(size=size)

    def choose_move(self, board):
        return choice(self.directions)