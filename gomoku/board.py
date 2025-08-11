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

    def checkLine(line):
        # Return early if provided line is too short
        if len(line) < 5:
            return False

        # Check for consecutively equal elements
        current = 0
        count = 0
        for piece in line:
            if piece == current:
                # Increment line length
                count += 1
                if count == 5 and current != 0:
                    # Non-empty line
                    return current
            else:
                # Start new line
                count = 1
                current = piece
        return 0

    def checkWin(self):
        # Check rows
        for i in range(15):
            win = self.checkLine(self.pieces[i])
            if win != 0:
                return win

        # Check columns
        for i in range(15):
            column = [self.pieces[j][i] for j in range(15)]
            win = self.checkLine(column)
            if win != 0:
                return win

        # Check main diagonal
        for i in range(15):
            diagonal = []
            x = 0
            y = i
            while y <= 14:
                diagonal.append(self.pieces[y][x])
                x += 1
                y += 1
            win = self.checkLine(diagonal)
            if win != 0:
                return win

        for i in range(1, 15):
            diagonal = []
            x = i
            y = 0
            while x <= 14:
                diagonal.append(self.pieces[y][x])
                x += 1
                y += 1
            win = self.checkLine(diagonal)
            if win != 0:
                return win

        # Check counter diagonal
        for i in range(15):
            diagonal = []
            x = 0
            y = i
            while y >= 0:
                diagonal.append(self.pieces[y][x])
                x += 1
                y -= 1
            win = self.checkLine(diagonal)
            if win != 0:
                return win

        for i in range(1, 15):
            diagonal = []
            x = i
            y = 14
            while x < 15:
                diagonal.append(self.pieces[y][x])
                x += 1
                y -= 1
            win = self.checkLine(diagonal)
            if win != 0:
                return win

        # Check draw
        full = True
        for y in range(15):
            for x in range(15):
                if self.pieces[y][x] == 0:
                    full = False
                    break
            if not full:
                break
        if full:
            # Pieces found, return tie
            return -1

        # No result, game has not ended
        return 0
