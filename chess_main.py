from board_logic import Board
import setup_tools

import tkinter as tk
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--setup", type=str, default="play", help="choose starting positions")

args = parser.parse_args()

root = tk.Tk()
board = Board(root, size=8)
root.bind("z", lambda e: board.undo_move())
root.bind("y", lambda e: board.redo_move())
if args.setup != "play":
    setup_tools.setup_locations(board, setup_tools.setups[args.setup])
root.mainloop()
