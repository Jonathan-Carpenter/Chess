from board_logic import Board
import tkinter as tk
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--setup", type=str, default="play", help="choose starting positions")

args = parser.parse_args()

# White pieces: ♔♕♖♗♘♙
# Black pieces: ♚♛♜♝♞♟

# Each entry in setups has a name as its key, and a list of moves as its value.
# A move is a dict which specifies the piece to move, which piece it is
# (i.e. Bishop 1 is the first Bishop we get to in the list of cells), the
# piece's colour, and the location it should move to.
setups = ({
    "checkmate1": ([
        {"piece": "♕", "which": 1, "colour": "w", "location": [3,0]},
        {"piece": "♗", "which": 2, "colour": "w", "location": [4,5]}
    ]),
    "check1": ([
        {"piece": "♕", "which": 1, "colour": "w", "location": [5,3]}
    ])
})

def exec_move(board, move_info):
    p_name, which, colour, location = move_info["piece"], move_info["which"], move_info["colour"], move_info["location"]
    for row in board.cells:
        for cell in row:
            if (cell.piece != None
                    and cell.piece.name[colour] == p_name
                    and cell.piece.colour == colour):
                which -= 1
                if which == 0: cell.piece.move(board.cells[location[0]][location[1]])

def setup_locations(board, move_dicts):
    for move_dict in move_dicts:
        exec_move(board, move_dict)

root = tk.Tk()
board = Board(root, size=8)
if args.setup != "play":
    setup_locations(board, setups[args.setup])
root.mainloop()
