import tkinter as tk
import random


class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048 Game")
        self.master.geometry("400x500")
        self.grid_size = 4
        self.board = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.colors = {
            0: "#CCC0B3", 2: "#EEE4DA", 4: "#EDE0C8", 8: "#F2B179",
            16: "#F59563", 32: "#F67C5F", 64: "#F65E3B", 128: "#EDCF72",
            256: "#EDCC61", 512: "#EDC850", 1024: "#EDC53F", 2048: "#EDC22E"
        }

        self.create_widgets()
        self.new_game()

    def create_widgets(self):
        # Frame for the game board
        self.game_frame = tk.Frame(self.master, bg="#BBADA0", width=400, height=400)
        self.game_frame.pack(pady=20)

        self.cells = []
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                cell = tk.Label(
                    self.game_frame,
                    text="",
                    bg=self.colors[0],
                    font=("Arial", 24, "bold"),
                    width=4,
                    height=2
                )
                cell.grid(row=i, column=j, padx=5, pady=5)
                row.append(cell)
            self.cells.append(row)

        # Frame for score and reset button
        self.control_frame = tk.Frame(self.master)
        self.control_frame.pack()

        self.score_label = tk.Label(
            self.control_frame, text=f"Score: {self.score}", font=("Arial", 16)
        )
        self.score_label.pack(side=tk.LEFT, padx=20)

        self.reset_button = tk.Button(
            self.control_frame, text="New Game", command=self.new_game, font=("Arial", 14)
        )
        self.reset_button.pack(side=tk.RIGHT, padx=20)

        self.master.bind("<Key>", self.handle_keypress)

    def new_game(self):
        self.board = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.add_random_tile()
        self.add_random_tile()
        self.update_ui()

    def add_random_tile(self):
        empty_cells = [
            (i, j)
            for i in range(self.grid_size)
            for j in range(self.grid_size)
            if self.board[i][j] == 0
        ]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = random.choice([2, 4])

    def update_ui(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = self.board[i][j]
                self.cells[i][j].config(
                    text=str(value) if value != 0 else "",
                    bg=self.colors.get(value, "#3C3A32")
                )
        self.score_label.config(text=f"Score: {self.score}")

    def compress(self, board):
        new_board = [[0] * self.grid_size for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            pos = 0
            for j in range(self.grid_size):
                if board[i][j] != 0:
                    new_board[i][pos] = board[i][j]
                    pos += 1
        return new_board

    def merge(self, board):
        for i in range(self.grid_size):
            for j in range(self.grid_size - 1):
                if board[i][j] == board[i][j + 1] and board[i][j] != 0:
                    board[i][j] *= 2
                    self.score += board[i][j]
                    board[i][j + 1] = 0
        return board

    def reverse(self, board):
        return [row[::-1] for row in board]

    def transpose(self, board):
        return [list(row) for row in zip(*board)]

    def move_left(self):
        new_board = self.compress(self.board)
        new_board = self.merge(new_board)
        new_board = self.compress(new_board)
        self.board = new_board

    def move_right(self):
        self.board = self.reverse(self.board)
        self.move_left()
        self.board = self.reverse(self.board)

    def move_up(self):
        self.board = self.transpose(self.board)
        self.move_left()
        self.board = self.transpose(self.board)

    def move_down(self):
        self.board = self.transpose(self.board)
        self.move_right()
        self.board = self.transpose(self.board)

    def handle_keypress(self, event):
        key_map = {
            "Left": self.move_left,
            "Right": self.move_right,
            "Up": self.move_up,
            "Down": self.move_down
        }
        if event.keysym in key_map:
            prev_board = [row[:] for row in self.board]
            key_map[event.keysym]()
            if prev_board != self.board:
                self.add_random_tile()
                self.update_ui()
            if not self.can_move():
                self.game_over()

    def can_move(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.board[i][j] == 0:
                    return True
                if j < self.grid_size - 1 and self.board[i][j] == self.board[i][j + 1]:
                    return True
                if i < self.grid_size - 1 and self.board[i][j] == self.board[i + 1][j]:
                    return True
        return False

    def game_over(self):
        game_over_label = tk.Label(
            self.master,
            text="Game Over!",
            font=("Arial", 24, "bold"),
            fg="red"
        )
        game_over_label.pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
