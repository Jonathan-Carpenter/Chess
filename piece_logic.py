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

    def get_moves(self):
        r, c = self.location[0], self.location[1]

        moves = []
        movements = self.movements.copy()

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
    def is_valid_move(self, move) -> (bool, bool):
        if move == [0,0]: return (False, False)

        new_location = [move[0] + self.location[0], move[1] + self.location[1]]
        valid = (True, True)

        # Can't move off the board
        if (new_location[0] >= self.board.size or new_location[0] < 0
         or new_location[1] >= self.board.size or new_location[1] < 0):
            valid = (False, False)
        # Can't move onto our own piece
        else:
            target_piece = self.board.cells[new_location[0]][new_location[1]].piece
            if target_piece != None:
                 if target_piece.colour == self.colour: valid = (False, False)
                 else: valid = (True, False)

        # if valid:
        #     print("Moving to {} is a valid move. Piece there is {}.".format(new_location, str(target_piece)))
        # else:
        #     print("Moving to {} is an invalid move. Piece there is {}.".format(new_location, str(target_piece)))

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

        if location[0] < 2: self.movements = [[1,0], [2,0]]
        else: self.movements = [[-1,0], [-2,0]]

        self.is_bounded = True
        self.can_jump = False
        super().__init__(board, cell, self.name, colour, location, self.movements, self.is_bounded, self.can_jump)
