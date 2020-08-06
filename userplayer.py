from tkinter import StringVar

from player import Player


class UserPlayer(Player):
    def __init__(self, win, size=4):
        super().__init__(size=size)
        self.keys = {}
        self._win = win
        self._direction = StringVar()
        self._win.bind('<Left>', lambda event: self._direction.set('left'))
        self._win.bind('<Right>', lambda event: self._direction.set('right'))
        self._win.bind('<Up>', lambda event: self._direction.set('up'))
        self._win.bind('<Down>', lambda event: self._direction.set('down'))

    def choose_move(self, board):
        self._win.wait_variable(self._direction)
        _dir = self._direction.get()
        self._direction.set(None)
        return _dir
