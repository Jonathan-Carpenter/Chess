from piece_logic import *
import tkinter as tk

class Cell:
    def __init__(self, location, widget=None, piece=None):
        self.location = location
        self.widget = widget
        self.piece = piece

    def __str__(self):
        if self.piece == None: return ""
        else: return self.piece.name[self.piece.colour]

    def update_entry(self):
        self.widget["text"] = str(self)
        self.widget.update()

class Board:
    def __init__(self, master, size, cell_size=1, font_size=50, font_name="Helvetica", active_colour="gray80", w_square_colour="sandy brown", b_square_colour="saddle brown"):
        self.master = master
        self.size = size
        self.cell_size = cell_size
        self.font_size = font_size
        self.font_name = font_name
        self.active_colour = active_colour
        self.w_square_colour = w_square_colour
        self.b_square_colour = b_square_colour
        self.active_piece = None
        self.init_cells()
        self.init_pieces()

    def init_cells(self):
        self.cells = []
        for r in range(self.size):
            self.cells.append([])
            for c in range(self.size):
                self.cells[r].append(Cell([r,c]))
                self.init_cell([r,c])

    def init_cell(self, location):
        r, c = location[0], location[1]
        cell = self.cells[r][c]

        if (r+c)%2 == 0:
            bg = self.b_square_colour
        else:
            bg = self.w_square_colour

        cell.widget = tk.Label(self.master, text=str(cell),
            width=self.cell_size*2, height=self.cell_size,
            font=(self.font_name, self.font_size),
            background=bg)
        cell.widget.grid(row=r, column=c)
        cell.widget.bind("<Button-1>", lambda e: self.click_handler(cell))

    def init_pieces(self):
        for r in range(self.size):
            for c in range(self.size):
                cell = self.cells[r][c]

                if r < 2: colour = "b"
                else: colour = "w"

                if r == 0 or r == self.size-1:
                    if c == 0 or c == self.size-1: cell.piece = Rook(self, cell, colour, [r,c])
                    elif c == 1 or c == self.size-2: cell.piece = Knight(self, cell, colour, [r,c])
                    elif c == 2 or c == self.size-3: cell.piece = Bishop(self, cell, colour, [r,c])
                    elif c == 3: cell.piece = King(self, cell, colour, [r,c])
                    elif c == 4: cell.piece = Queen(self, cell, colour, [r,c])
                elif r == 1 or r == self.size-2:
                    cell.piece = Pawn(self, cell, colour, [r,c])

                cell.widget["text"] = str(cell)

    def click_handler(self, cell):
        # print("\nClicked on cell {}".format(cell.location))
        if self.active_piece == None and cell.piece == None:
            return

        elif self.active_piece == None:
            self.active_piece = cell.piece
            cell.orig_colour = cell.widget["bg"]
            cell.widget["bg"] = self.active_colour

            # print("\nActive piece is now {}.".format(str(self.active_piece)))

            moves = cell.piece.get_moves()
            self.valid_cells = []
            for move in moves:
                self.valid_cells.append([move[0] + cell.location[0], move[1] + cell.location[1]])

            # print("Valid cells to move to: {}.".format(self.valid_cells))

        elif cell.location not in self.valid_cells:
            self.active_piece.cell.widget["bg"] = self.active_piece.cell.orig_colour
            self.active_piece = None

        else:
            self.move_handler(cell)

    def move_handler(self, cell):
        # print("Move piece at {} to {}".format(self.active_piece.location, cell.location))
        if self.active_piece.name["w"] == "♙" and len(self.active_piece.movements)>1: del self.active_piece.movements[1]

        cell.piece = self.active_piece.cell.piece
        cell.update_entry()

        self.active_piece.cell.piece = None
        self.active_piece.cell.update_entry()
        self.active_piece.cell.widget["bg"] = self.active_piece.cell.orig_colour

        self.active_piece.cell = cell
        self.active_piece.location = cell.location

        self.active_piece = None
