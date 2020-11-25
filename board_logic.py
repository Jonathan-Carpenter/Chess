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
    def __init__(self, master, cell_size=1, font_size=50,
            font_name="Helvetica", valid_text="·", active_colour="gray80",
            w_square_colour="sandy brown", b_square_colour="saddle brown",
            check_colour="yellow", checkmate_colour="red"):
        self.master = master
        self.size = 8
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

        self.move_history = []
        self.move_future = []

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

        if (r+c)%2 == 1:
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
        cell.prev_colour = bg

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
                    elif c == 4:
                        cell.piece = King(self, cell, colour, [r,c])
                        self.kings[colour] = cell.piece
                    elif c == 3: cell.piece = Queen(self, cell, colour, [r,c])
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
            if cell.orig_colour == None: cell.orig_colour = cell.widget["bg"]
            cell.prev_colour = cell.widget["bg"]
            cell.widget["bg"] = self.active_colour

            moves = cell.piece.get_moves()
            self.valid_locations = []
            for move in moves:
                self.valid_locations.append([move[0] + cell.location[0], move[1] + cell.location[1]])

            self.paint_valid_locations(self.valid_text)

        # If there is an active piece, but we do not click a valid location,
        # do nothing but clear up the UI, and forget the active piece.
        elif cell.location not in self.valid_locations:
            self.active_piece.cell.widget["bg"] = self.active_piece.cell.prev_colour
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
        taken_piece = cell.piece
        move_made = [cell.location[0] - self.active_piece.location[0], cell.location[1] - self.active_piece.location[1]]

        if not self.test_move_for_check(cell):
            self.active_piece.move(cell)
            self.paint_valid_locations(orig=True)
        else:
            print("You can't make a move that puts your king in check!")
            self.active_piece = None
            return

        self.move_history.append([[self.active_piece, old_cell]])

        # Check for en passent, put taken pawn in history and update its square
        if taken_piece == None and self.active_piece.name["w"]=="♙" and move_made in self.active_piece.takes:
            taken_piece = self.cells[cell.location[0] - self.active_piece.orig_movements[0][0]][cell.location[1]].piece
            self.move_history[-1].append([taken_piece, taken_piece.cell])
            taken_piece.cell.piece = None
            taken_piece.cell.update_entry()
            taken_piece = None

        # If this piece is a king and we are moving two squares,
        # move the rook as well, and add both to move history
        if self.active_piece == self.kings[self.active_player]:
            if cell.location[1] - old_cell.location[1] > 1:
                self.move_rook(2, self.cells[cell.location[0]][cell.location[1]-1])
            elif cell.location[1] - old_cell.location[1] < -1:
                self.move_rook(1, self.cells[cell.location[0]][cell.location[1]+1])

        if taken_piece != None: self.move_history[-1].append([taken_piece, cell])
        self.move_future = []
        self.active_piece = None

        # If the move went ahead, switch players
        self.switch_players()

        # If the new player is in check, then test if they are in checkmate
        if self.in_check(self.active_player, draw=True) and self.checkmate(self.active_player):
            if self.active_player == "w": win_msg = "Black "
            else: win_msg = "White "
            win_msg += "wins by checkmate!"
            print(win_msg)
            self.active_player = None

    def move_rook(self, which, cell):
        for r in self.cells:
            for c in r:
                if c.piece != None and c.piece.name["w"] == "♖" and c.piece.colour == self.active_player:
                    which -= 1
                    if which == 0:
                        self.move_history[-1].append([c.piece, c])
                        c.piece.move(cell)

    def in_check(self, player, draw=False):
        check = self.kings[player].is_threatened()[0]
        if draw:
            if check:
                self.kings[player].cell.widget["bg"] = self.check_colour
            else:
                self.kings[player].cell.widget["bg"] = self.kings[player].cell.orig_colour
        return check

    def test_move_for_check(self, cell, draw=False):
        check = False
        old_cell = self.active_piece.cell
        self.active_piece.move(cell)
        if self.in_check(self.active_piece.colour, draw):
            self.active_piece.move(old_cell)
            if draw: self.active_piece.cell.widget["bg"] = self.active_piece.cell.prev_colour
            check = True
        self.active_piece.move(old_cell)
        return check

    def stalemate(self):
        for row in self.cells:
            for cell in row:
                self.active_piece = cell.piece
                moves = cell.piece.get_moves()
                self.valid_locations = []
                for move in moves:
                    self.valid_locations.append([move[0] + cell.location[0], move[1] + cell.location[1]])
                for loc in self.valid_locations:
                    dest_cell = self.cells[loc[0]][loc[1]]
                    if not self.test_move_for_check(dest_cell):
                        self.active_piece = None
                        return False
        self.active_piece = None
        return True

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
                    if not checkmated:
                        return False

        self.kings[player].cell.widget["bg"] = self.checkmate_colour
        return True

    def unredo_move(self, mode):
        if mode == "undo":
            pop_from, push_to = self.move_history, self.move_future
        elif mode == "redo":
            pop_from, push_to = self.move_future, self.move_history

        if self.active_player == None or pop_from == []:
            return

        moves = pop_from.pop()
        push_to.append([])
        castling = len(moves)>1 and moves[0][0].colour == moves[1][0].colour
        for i, move in enumerate(moves):
            push_to[-1].append([move[0], move[0].cell])
            if mode != "redo" or i == 0 or castling: move[0].move(move[1], unredo=True)

        self.in_check(self.active_player, draw=True)
        self.switch_players()
        self.in_check(self.active_player, draw=True)

    def switch_players(self):
        if self.stalemate():
            print("Draw by stalemate!")
            self.active_player = None

        if self.active_player == "w":
            self.active_player = "b"
        else:
            self.active_player = "w"
