# tkinter Chess Game

Chess game for two human players (move pieces with mouse). The implementation currently includes the following:
- Players take turns, only being able to move their own pieces.
- Selecting a piece highlights that square and displays the possible moves.
- The game tests for **check** and **checkmate**.
- Making a move which leads to check, or fails to block an existing check, is prevented.
- When a king is in check, his square is highlighted yellow. Similarly, it is highlighted red for checkmate.
- Moves can be **undone** and **redone** using the 'z' and 'y' keys, respectively.
- Special moves implemented so far (both can be undone and redone):
    - **castling**, including not being able to castle out of check (select the king, not the rook, to perform this move),
    - **promotion** for pawns which reach the other side of the board (choose new piece by responding in the console).

TODO:
- Extend UI so that valid moves are highlighted when a piece is selected -- DONE
- Implement castling (DONE) and en passant
- Implement promotion -- DONE
- Implement check and checkmate, incl. can't move into check -- DONE
- Implement stalemate
- Design AI opponent
