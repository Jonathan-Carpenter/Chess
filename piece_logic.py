class Piece:
    # Movements holds the moves that a particular piece can make, ignoring its location and surroundings
    # is_bounded is a flag which is False if the piece can move an infinite distance, e.g. Queen, Bishop, Rook, and false otherwise
    def __init__(self, master, name, colour, location, movements, is_bounded, can_jump):
        self.master = master
        self.name = name
        self.colour = colour
        self.location = location
        self.movements = movements
        self.is_bounded = is_bounded
        self.can_jump = can_jump

    def __str__(self):
        return self.colour + self.name

    def get_moves(self):
        r, c = self.location[0], self.location[1]

        moves = []
        movements = self.movements.copy()

        if not self.is_bounded:
            max_mult = self.master.size
        else:
            max_mult = 1

        for move_mult in range(1, max_mult+1):
            for i, move in enumerate(movements):
                scaled_move = [move[0]*move_mult, move[1]*move_mult]
                if self.is_valid_move(scaled_move):
                    moves.append(scaled_move)
                else:
                    # We must have hit our own piece, or the edge of the board,
                    # so don't try to move that way again.
                    if not self.can_jump: movements[i] = [0,0]

        return moves

    def is_valid_move(self, move):
        if move == [0,0]: return False

        new_location = [move[0] + self.location[0], move[1] + self.location[1]]
        valid = True

        # Can't move off the board
        if (new_location[0] >= self.master.size or new_location[0] < 0
         or new_location[1] >= self.master.size or new_location[1] < 0):
            valid = False
            return valid
        # Can't move onto our own piece
        else:
            target_piece = self.master.cells[new_location[0]][new_location[1]].piece
            if target_piece != None and target_piece.colour == self.colour:
                valid = False

        if valid:
            print("Moving to {} is a valid move. Piece there is {}.".format(new_location, str(target_piece)))
        else:
            print("Moving to {} is an invalid move. Piece there is {}.".format(new_location, str(target_piece)))

        return valid

class Rook(Piece):
    def __init__(self, master, colour, location):
        self.name = "Ro"
        self.movements = [[1,0], [-1,0], [0,1], [0,-1]]
        self.is_bounded = False
        self.can_jump = False
        super().__init__(master, self.name, colour, location, self.movements, self.is_bounded, self.can_jump)

class Knight(Piece):
    def __init__(self, master, colour, location):
        self.name = "Kn"
        self.movements = ([
            [1,-2], [1,2], [2,-1], [2,1],
            [-1,-2], [-1,2], [-2,-1], [-2,1]
        ])
        self.is_bounded = True
        self.can_jump = True
        super().__init__(master, self.name, colour, location, self.movements, self.is_bounded, self.can_jump)

class Bishop(Piece):
    def __init__(self, master, colour, location):
        self.name = "Bi"
        self.movements = [[1,1], [-1,-1], [1,-1], [-1,1]]
        self.is_bounded = False
        self.can_jump = False
        super().__init__(master, self.name, colour, location, self.movements, self.is_bounded, self.can_jump)

class King(Piece):
    def __init__(self, master, colour, location):
        self.name = "Ki"
        self.movements = [[1,0], [-1,0], [0,1], [0,-1]]
        self.is_bounded = True
        self.can_jump = False
        super().__init__(master, self.name, colour, location, self.movements, self.is_bounded, self.can_jump)

class Queen(Piece):
    def __init__(self, master, colour, location):
        self.name = "Qu"
        self.movements = ([
            [1,0], [-1,0], [0,1], [0,-1],
            [1,1], [-1,-1], [1,-1], [-1,1]
        ])
        self.is_bounded = False
        self.can_jump = False
        super().__init__(master, self.name, colour, location, self.movements, self.is_bounded, self.can_jump)

class Pawn(Piece):
    def __init__(self, master, colour, location):
        self.name = "Pa"

        if location[0] < 2: self.movements = [[1,0], [2,0]]
        else: self.movements = [[-1,0], [-2,0]]

        self.is_bounded = True
        self.can_jump = False
        super().__init__(master, self.name, colour, location, self.movements, self.is_bounded, self.can_jump)
