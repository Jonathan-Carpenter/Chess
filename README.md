# tkinter Chess Game

Chess game for two human players (move pieces with mouse). The implementation currently includes the following:
- Players take turns, only being able to move their own pieces.
- Selecting a piece highlights that square and displays the possible moves.
- The game tests for **check** and **checkmate**.
- Making a move which leads to check, or fails to block an existing check, is prevented.
- When a king is in check, his square is highlighted yellow. Similarly, it is highlighted red for checkmate.
- Moves can be **undone** and **redone** using the 'z' and 'y' keys, respectively.

TODO:
- Extend UI so that valid moves are highlighted when a piece is selected -- DONE
- Implement castling (DONE) and en passant
- Implement promotion
- Implement check and checkmate, incl. can't move into check -- DONE
- Implement stalemate
- Design AI opponent
