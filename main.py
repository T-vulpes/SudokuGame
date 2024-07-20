import tkinter as tk
from tkinter import messagebox
import random

class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver and Generator")

        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.entries = [[None for _ in range(9)] for _ in range(9)]

        self.create_widgets()
        self.generate_sudoku(40)  # Generate a sudoku puzzle with 40 holes

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack()

        for i in range(9):
            for j in range(9):
                entry = tk.Entry(frame, width=3, font=('Arial', 18), justify='center')
                entry.grid(row=i, column=j, padx=1, pady=1)
                entry.bind('<KeyRelease>', self.check_input)
                self.entries[i][j] = entry

                if (i // 3 + j // 3) % 2 == 0:
                    entry.configure(bg='#f0f0f0')
                else:
                    entry.configure(bg='#ffffff')

        solve_button = tk.Button(self.root, text="Solve", command=self.solve)
        solve_button.pack(side=tk.LEFT, padx=10, pady=10)

        generate_button = tk.Button(self.root, text="Generate", command=lambda: self.generate_sudoku(40))
        generate_button.pack(side=tk.LEFT, padx=10, pady=10)

        clear_button = tk.Button(self.root, text="Clear", command=self.clear)
        clear_button.pack(side=tk.LEFT, padx=10, pady=10)

    def solve(self):
        self.update_board_from_entries()
        if solve_sudoku(self.board):
            self.update_entries_from_board()
        else:
            messagebox.showerror("Error", "No solution exists")

    def generate_sudoku(self, num_holes):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        fill_diagonal_boxes(self.board)
        solve_sudoku(self.board)
        remove_numbers(self.board, num_holes)
        self.update_entries_from_board()

    def clear(self):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].config(bg='#f0f0f0' if (i // 3 + j // 3) % 2 == 0 else '#ffffff')
        self.board = [[0 for _ in range(9)] for _ in range(9)]

    def update_board_from_entries(self):
        for i in range(9):
            for j in range(9):
                value = self.entries[i][j].get()
                self.board[i][j] = int(value) if value.isdigit() else 0

    def update_entries_from_board(self):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                if self.board[i][j] != 0:
                    self.entries[i][j].insert(0, str(self.board[i][j]))

    def check_input(self, event):
        entry = event.widget
        value = entry.get()
        if not value.isdigit() or int(value) < 1 or int(value) > 9:
            entry.config(bg='red')
        else:
            row, col = None, None
            for i in range(9):
                for j in range(9):
                    if self.entries[i][j] == entry:
                        row, col = i, j
                        break
            if is_valid(self.board, row, col, int(value)):
                entry.config(bg='#f0f0f0' if (row // 3 + col // 3) % 2 == 0 else '#ffffff')
                self.board[row][col] = int(value)
                if not find_empty(self.board):
                    messagebox.showinfo("Game Over", "Congratulations! You've completed the Sudoku.")
            else:
                entry.config(bg='red')

def print_board(board):
    for row in board:
        print(" ".join(str(num) if num != 0 else '.' for num in row))

def is_valid(board, row, col, num):
    if num in board[row]:
        return False

    if num in [board[i][col] for i in range(9)]:
        return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def solve_sudoku(board):
    empty_pos = find_empty(board)
    if not empty_pos:
        return True

    row, col = empty_pos

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num

            if solve_sudoku(board):
                return True

            board[row][col] = 0

    return False

def fill_diagonal_boxes(board):
    for i in range(0, 9, 3):
        fill_3x3_box(board, i, i)

def fill_3x3_box(board, row, col):
    nums = list(range(1, 10))
    random.shuffle(nums)
    for i in range(3):
        for j in range(3):
            board[row + i][col + j] = nums.pop()

def remove_numbers(board, num_holes):
    while num_holes > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if board[row][col] != 0:
            board[row][col] = 0
            num_holes -= 1

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()
