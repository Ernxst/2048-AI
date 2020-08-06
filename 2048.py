from tkinter import Frame, Label, Tk

from autoplayer import Autoplayer
from board import Board
from constants import BG_GAME, TILE_BG, TILE_FG, EMPTY_TILE, FONT
from randomplayer import RandomPlayer
from userplayer import UserPlayer


class UI(Frame):
    def __init__(self, parent, size=4, width=500, height=500):
        super().__init__(parent, bg=BG_GAME, width=width, height=height)
        self.grid_propagate(0)
        self.size, self.board = size, Board(size)
        self.cells = [[Label(self, font=FONT, text='', bg=EMPTY_TILE) for _ in range(size)] for _ in range(size)]

    def grid(self, **kwargs):
        super(Frame, self).grid(**kwargs)
        for i in range(self.size):
            self.rowconfigure(i, weight=1, uniform='rows')
            self.columnconfigure(i, weight=1, uniform='rows')
            for j in range(self.size):
                self.cells[i][j].grid(row=i, column=j, padx=5, pady=5, sticky='nesw')
        self.update()

    def update(self):
        super(Frame, self).update()
        for i in range(self.size):
            for j in range(self.size):
                num = self.board.board[i][j]
                if num == 0:
                    self.cells[i][j].config(text="", bg=EMPTY_TILE)
                else:
                    self.cells[i][j].config(text=str(num), bg=TILE_BG[num], fg=TILE_FG[num])

    def move(self, direction):
        if self.board.move(direction) != -1:
            if not self.is_game_over():
                self.board.spawn_tile()
        self.update()
        self.end_game()

    def is_game_over(self):
        return self.board.state() != 'not over'

    def end_game(self):
        state = self.board.state()
        if state == 'win':
            self.cells[1][1].config(text="You", bg=EMPTY_TILE, fg='green')
            self.cells[1][2].config(text="Win!", bg=EMPTY_TILE, fg='green')
        elif state == 'lose':
            self.cells[1][1].config(text="You", bg=EMPTY_TILE, fg='red')
            self.cells[1][2].config(text="Lose!", bg=EMPTY_TILE, fg='red')


def test(size=5):
    game = UI(win, size=size)
    game.grid(sticky='nesw')
    ai = RandomPlayer(size)
    while not game.is_game_over():
        game.move(ai.choose_move(game.board))
        game.after(250)


if __name__ == "__main__":
    win = Tk()
    test()
    win.mainloop()
