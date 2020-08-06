from random import choice, randrange


class Board:
    def __init__(self, size=4):
        self.size, self.board = size, None
        self.directions = {"left": self.left, "right": self.right, "up": self.up, "down": self.down}
        self.new_game()

    def clone(self):
        board = Board(self.size)
        board.board = [row[:] for row in self.board]
        return board

    def new_game(self):
        self.board = [[0] * self.size for _ in range(self.size)]
        self.spawn_tile()
        self.spawn_tile()

    def find_empty_tiles(self):
        empty_tiles = []
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 0:
                    empty_tiles.append((row, col))
        return empty_tiles

    def get_next_tile(self):
        empty_tiles = self.find_empty_tiles()
        if len(empty_tiles) > 0:
            return choice(empty_tiles)
        return None, None

    def spawn_tile(self):
        new_tile = 4 if randrange(100) > 89 else 2
        a, b = self.get_next_tile()
        if a is not None and b is not None:
            self.board[a][b] = new_tile

    def state(self):
        if not len(self.find_empty_tiles()) == 0:
            return 'not over'
        if sorted(sum(self.board, []))[-1] >= 2048:
            return 'win'
        test_board = self.clone()
        test_board.merge()
        if test_board.board != self.board:
            return 'not over'
        return 'lose'

    def reverse(self):
        self.board = [row[::-1] for row in self.board[::-1]]

    def transpose(self):
        self.board = list(map(list, zip(*self.board)))

    def merge(self):
        merges = 0
        for i in range(self.size):
            for j in range(self.size - 1):
                if self.board[i][j] == self.board[i][j + 1]:
                    self.merge_tiles(i, j)
                    merges += 1
        for i in range(self.size - 1):
            for j in range(self.size):
                if self.board[i][j] == self.board[i + 1][j] and self.board[i][j] != 0:
                    self.merge_tiles(i, j, x_shift=0, y_shift=1)
                    merges += 1
        return merges

    def merge_tiles(self, i, j, x_shift=1, y_shift=0):
        self.board[i][j] *= 2
        self.board[i + y_shift][j + x_shift] = 0

    def valid_move(self, direction):
        test_board = self.clone()
        test_board.directions[direction]()
        test_board.merge()
        return test_board.board != self.board

    def move(self, direction):
        if self.valid_move(direction):
            self.directions[direction]()
            return self.merge()
        return -1

    def up(self):
        self.transpose()
        self.left()
        self.transpose()

    def down(self):
        self.transpose()
        self.right()
        self.transpose()

    def left(self):
        for i in range(self.size):
            new_row = [j for j in self.board[i] if j != 0]
            self.board[i] = new_row + [0 for _ in range(self.size - len(new_row))]

    def right(self):
        self.reverse()
        self.left()
        self.reverse()
