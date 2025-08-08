class Board:
    def __init__(self):
        # List comprehension to make a 15x15 2D array of zeros
        self.pieces = [[0 for _ in range(15)] for _ in range(15)]

        # Store order of placed pieces
        self.history = []
        # Store which player is to play the next move
        self.currentPlayer = 1

    def getPiece(self, x, y):
        return self.pieces[y][x]

    def positionEmpty(self, x, y):
        # Check whether the specified cell is available to place a piece
        return self.getPiece(x, y) == 0

    def swapPlayer(self):
        # Change the current player
        if self.currentPlayer == 1:
            self.currentPlayer = 2
        elif self.currentPlayer == 2:
            self.currentPlayer = 1

    def playPiece(self, x, y):
        # Attempt to place a piece, return True if successful
        # and False otherwise
        if x < 0 or x > 14:
            return False
        if y < 0 or y > 15:
            return False

        if self.positionEmpty(x, y):
            self.pieces[y][x] = self.currentPlayer
            self.swapPlayer()
            return True
        else:
            return False
