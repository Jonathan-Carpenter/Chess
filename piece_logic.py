class Piece:
    # Movements holds the moves that a particular piece can make, ignoring its location and surroundings
    # is_bounded is a flag which is False if the piece can move an infinite distance, e.g. Queen, Bishop, Rook, and false otherwise
    def __init__(self, board, cell, name, colour, location, movements, is_bounded, can_jump):
        self.board = board
        self.cell = cell
        self.name = name
        self.colour = colour
        self.location = location
        self.movements = movements
        self.is_bounded = is_bounded
        self.can_jump = can_jump

    def __str__(self):
        return self.name[self.colour]

    def move(self, cell, draw=True, unredo=False):
        # remove piece from current cell, and print
        self.cell.piece = None
        if draw: self.cell.update_entry()
        if draw: self.cell.widget["bg"] = self.cell.orig_colour

        # set piece of destination, and print
        cell.piece = self
        if draw: cell.update_entry()

        # update cell and location attributes to destination
        self.cell = cell
        self.location = cell.location

    def is_threatened(self):
        threatened = False
        threats = []

        for row in self.board.cells:
            for cell in row:
                if cell.piece == None:
                    continue
                if cell.piece.colour != self.colour:
                    enemy_moves = cell.piece.get_moves()
                    for move in enemy_moves:
                        location = [cell.location[0]+move[0], cell.location[1]+move[1]]
                        if location == self.location:
                            threatened = True
                            threats.append(cell.location)
        return (threatened, threats)

    def get_moves(self, moves=None, movements=None):
        r, c = self.location[0], self.location[1]

        if moves == None: moves = []
        if movements == None: movements = self.movements.copy()

        if not self.is_bounded:
            max_mult = self.board.size
        else:
            max_mult = 1

        for move_mult in range(1, max_mult+1):
            for i, move in enumerate(movements):
                scaled_move = [move[0]*move_mult, move[1]*move_mult]
                valid = self.is_valid_move(scaled_move)
                if valid[0]:
                    moves.append(scaled_move)
                if not valid[1]:
                    # We must have hit our own piece, or the edge of the board,
                    # so don't try to move that way again.
                    if not self.can_jump: movements[i] = [0,0]

        return moves

    # return type signifies (can I move there?, can I keep moving in that direction?)
    def is_valid_move(self, move, is_take=False) -> (bool, bool):
        if move == [0,0]: return (False, False)

        new_location = [move[0] + self.location[0], move[1] + self.location[1]]
        valid = (not is_take, not is_take)

        # Can't move off the board
        if (new_location[0] >= self.board.size or new_location[0] < 0
         or new_location[1] >= self.board.size or new_location[1] < 0):
            valid = (False, False)
        else:
            target_piece = self.board.cells[new_location[0]][new_location[1]].piece
            if target_piece != None:
                # Can't move onto our own piece
                 if target_piece.colour == self.colour: valid = (False, False)
                 else: valid = (True, False)

        return valid

class Rook(Piece):
    def __init__(self, board, cell, colour, location):
        self.name = {"w": "♖", "b": "♜"}
        self.movements = [[1,0], [-1,0], [0,1], [0,-1]]
        self.is_bounded = False
        self.can_jump = False
        super().__init__(board, cell, self.name, colour, location, self.movements, self.is_bounded, self.can_jump)

class Knight(Piece):
    def __init__(self, board, cell, colour, location):
        self.name = {"w": "♘", "b": "♞"}
        self.movements = ([
            [1,-2], [1,2], [2,-1], [2,1],
            [-1,-2], [-1,2], [-2,-1], [-2,1]
        ])
        self.is_bounded = True
        self.can_jump = True
        super().__init__(board, cell, self.name, colour, location, self.movements, self.is_bounded, self.can_jump)

class Bishop(Piece):
    def __init__(self, board, cell, colour, location):
        self.name = {"w": "♗", "b": "♝"}
        self.movements = [[1,1], [-1,-1], [1,-1], [-1,1]]
        self.is_bounded = False
        self.can_jump = False
        super().__init__(board, cell, self.name, colour, location, self.movements, self.is_bounded, self.can_jump)

class King(Piece):
    def __init__(self, board, cell, colour, location):
        self.name = {"w": "♔", "b": "♚"}
        self.movements = ([
            [1,0], [-1,0], [0,1], [0,-1],
            [1,1], [-1,-1], [1,-1], [-1,1]
        ])
        self.is_bounded = True
        self.can_jump = False
        super().__init__(board, cell, self.name, colour, location, self.movements, self.is_bounded, self.can_jump)

    def get_moves(self):
        r, c = self.location[0], self.location[1]

        moves = []

        moved_pieces = [move[0] for move_set in self.board.move_history for move in move_set]

        moved_king = self in moved_pieces
        if moved_king or (self.board.active_player == self.colour and self.is_threatened()[0]):
            super().get_moves(moves)
            return moves

        rook_sq_piece = self.board.cells[r][c-3].piece
        moved_rook = rook_sq_piece in moved_pieces
        empty_between = self.board.cells[r][c-1].piece == None and self.board.cells[r][c-2].piece == None

        if (empty_between and rook_sq_piece != None
                and rook_sq_piece.name["w"] == "♖" and not moved_rook):
            moves.append([0,-2])

        rook_sq_piece = self.board.cells[r][c+4].piece
        moved_rook = rook_sq_piece in moved_pieces
        empty_between = (self.board.cells[r][c+1].piece == None
                        and self.board.cells[r][c+2].piece == None
                        and self.board.cells[r][c+3].piece == None)
        if (empty_between and rook_sq_piece != None
                and rook_sq_piece.name["w"] == "♖" and not moved_rook):
            moves.append([0,2])

        super().get_moves(moves)
        return moves

class Queen(Piece):
    def __init__(self, board, cell, colour, location):
        self.name = {"w": "♕", "b": "♛"}
        self.movements = ([
            [1,0], [-1,0], [0,1], [0,-1],
            [1,1], [-1,-1], [1,-1], [-1,1]
        ])
        self.is_bounded = False
        self.can_jump = False
        super().__init__(board, cell, self.name, colour, location, self.movements, self.is_bounded, self.can_jump)

class Pawn(Piece):
    def __init__(self, board, cell, colour, location):
        self.name = {"w": "♙", "b": "♟"}
        self.orig_location = location

        if location[0] < 2:
            self.orig_movements = [[1,0], [2,0]]
            self.takes = [[1,1], [1,-1]]
        else:
            self.orig_movements = [[-1,0], [-2,0]]
            self.takes = [[-1,1], [-1,-1]]

        self.movements = self.orig_movements

        self.is_bounded = True
        self.can_jump = False
        self.prom_choice = None
        super().__init__(board, cell, self.name, colour, location, self.movements, self.is_bounded, self.can_jump)

    def get_moves(self):
        if self.location == self.orig_location: self.movements = self.orig_movements
        else: self.movements = [self.orig_movements[0]]

        r, c = self.location[0], self.location[1]

        moves = []
        movements = self.movements.copy()

        if r == self.board.size-1 or (self.board.cells[r+1][c].piece != None and [1,0] in movements):
            movements.remove([1,0])
        elif r == 0 or (self.board.cells[r-1][c].piece != None and [-1,0] in movements):
            movements.remove([-1,0])
        for move in self.takes:
            if self.is_valid_move(move, is_take=True)[0]: moves.append(move)

        super().get_moves(moves, movements)
        return moves

    def move(self, cell, draw=True, unredo=False):
        super().move(cell, draw)
        piece_names = {'1': "bishop", '2': "knight", '3': "rook", '4': "queen"}
        piece_id = 0

        if self.location[0] == 0 or self.location[0] == self.board.size-1:
            if not unredo:
                print("Pawn promotion!")
                for id in piece_names:
                    print("\t{}. {}".format(id, piece_names[id]))
                while piece_id not in piece_names:
                    piece_id = input("Enter a number for pawn promotion: ")
                self.prom_choice = piece_id
            else:
                piece_id = self.prom_choice

            if piece_id == '1':
                cell.piece = Bishop(self.board, cell, self.board.active_player, cell.location)
            elif piece_id == '2':
                cell.piece = Knight(self.board, cell, self.board.active_player, cell.location)
            elif piece_id == '3':
                cell.piece = Rook(self.board, cell, self.board.active_player, cell.location)
            elif piece_id == '4':
                cell.piece = Queen(self.board, cell, self.board.active_player, cell.location)

            cell.update_entry()
