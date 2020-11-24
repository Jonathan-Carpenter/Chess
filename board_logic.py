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
    def __init__(self, master, size, cell_size=1, font_size=50,
            font_name="Helvetica", valid_text="·", active_colour="gray80",
            w_square_colour="sandy brown", b_square_colour="saddle brown",
            check_colour="yellow", checkmate_colour="red"):
        self.master = master
        self.size = size
        self.cell_size = cell_size
        self.font_size = font_size
        self.font_name = font_name
        self.valid_text = valid_text

        self.active_colour = active_colour
        self.check_colour = check_colour
        self.checkmate_colour = checkmate_colour
        self.w_square_colour = w_square_colour
        self.b_square_colour = b_square_colour

        self.active_piece = None
        self.active_player = "w"
        self.kings = {"w": None, "b": None}

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
        cell.orig_colour = bg

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
                    elif c == 3:
                        cell.piece = King(self, cell, colour, [r,c])
                        self.kings[colour] = cell.piece
                    elif c == 4: cell.piece = Queen(self, cell, colour, [r,c])
                elif r == 1 or r == self.size-2:
                    cell.piece = Pawn(self, cell, colour, [r,c])

                cell.widget["text"] = str(cell)

    def click_handler(self, cell):
        # There is no active piece and the clicked cell contains no piece
        # Nothing needs to be done; return
        if self.active_piece == None and (cell.piece == None
                or cell.piece.colour != self.active_player):
            return

        # Otherwise, if there is no active piece, set it to the one we clicked on.
        # Also show possible moves, and change colour of current cell.
        if self.active_piece == None:
            self.active_piece = cell.piece
            cell.orig_colour = cell.widget["bg"]
            cell.widget["bg"] = self.active_colour

            moves = cell.piece.get_moves()
            self.valid_locations = []
            for move in moves:
                self.valid_locations.append([move[0] + cell.location[0], move[1] + cell.location[1]])

            self.paint_valid_locations(self.valid_text)

        # If there is an active piece, but we do not click a valid location,
        # do nothing but clear up the UI, and forget the active piece.
        elif cell.location not in self.valid_locations:
            self.active_piece.cell.widget["bg"] = self.active_piece.cell.orig_colour
            self.active_piece = None
            self.paint_valid_locations(orig=True)

        # Otherwise, there must be an active piece and we must have clicked a valid location.
        # Move the piece and clear up the UI.
        else:
            self.move_handler(cell)
            self.paint_valid_locations(orig=True)

    # This function can insert chosen text in valid locations to make them visible to the user.
    # This needs to be undone afterwards in another call, and is done by setting orig=True.
    def paint_valid_locations(self, text=None, orig=False):
        for cell in self.valid_locations:
            r, c = cell[0], cell[1]
            if orig: text = ""
            if self.cells[r][c].piece == None: self.cells[r][c].widget["text"] = text

    def move_handler(self, cell):
        # TODO: when castling implemented --> you can't castle out of check

        old_cell = self.active_piece.cell
        self.active_piece.move(cell)

        # If the move put the player in check, undo and abort
        if self.in_check(self.active_player, draw=True):
            self.active_piece.move(old_cell)
            print("You can't make a move that puts your king in check!")
            self.active_piece = None
            return

        self.active_piece = None

        # If the move went ahead, switch players
        if self.active_player == "w":
            self.active_player = "b"
        else:
            self.active_player = "w"

        # If the new player is in check, then test if they are in checkmate
        if self.in_check(self.active_player, draw=True) and self.checkmate(self.active_player):
            if self.active_player == "w": win_msg = "Black "
            else: win_msg = "White "
            win_msg += "wins by checkmate!"
            print(win_msg)
            self.active_player = None

    def in_check(self, player, draw=False):
        check = self.kings[player].is_threatened()[0]
        if draw:
            if check:
                self.kings[player].cell.widget["bg"] = self.check_colour
            else:
                self.kings[player].cell.widget["bg"] = self.kings[player].cell.orig_colour
        return check

    def checkmate(self, player):
        checkmated = True
        for row in self.cells:
            for cell in row:
                piece = cell.piece
                if piece == None or piece.colour != player: continue
                moves = piece.get_moves()
                for move in moves:
                    # Convert move to new location
                    move[0] += cell.location[0]
                    move[1] += cell.location[1]

                    # Keep track of piece at destination
                    dest_piece = self.cells[move[0]][move[1]].piece

                    # Move piece there, test for check, and move back
                    piece.move(self.cells[move[0]][move[1]], draw=False)
                    if not self.in_check(player): checkmated = False
                    piece.move(cell, draw=False)

                    # Reset piece at destination, and return false if move removed check
                    self.cells[move[0]][move[1]].piece = dest_piece
                    if not checkmated: return False

        self.kings[player].cell.widget["bg"] = self.checkmate_colour
        return True
