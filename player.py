from abc import abstractmethod


class Player:
    def __init__(self, size=4):
        self.size, self.directions = size, ["up", "down", "left", "right"]

    @abstractmethod
    def choose_move(self, board):
        pass