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
        # Change the current player (1 becomes 2, 2 becomes 1)
        self.currentPlayer = 3 - self.currentPlayer

    def playPiece(self, x, y):
        # Attempt to place a piece, return True if successful
        # and False otherwise
        if x < 0 or x > 14:
            return False
        if y < 0 or y > 15:
            return False

        if self.positionEmpty(x, y):
            self.pieces[y][x] = self.currentPlayer
            self.history.append((x, y))
            self.swapPlayer()
            return True
        else:
            return False

    @staticmethod
    def checkLine(line):
        # Return early if provided line is too short
        if len(line) < 5:
            return 0

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
        # Return early if history is too short
        if len(self.history) < 9:
            return 0

        # Check rows
        for i in range(15):
            win = Board.checkLine(self.pieces[i])
            if win != 0:
                return win

        # Check columns
        for i in range(15):
            column = [self.pieces[j][i] for j in range(15)]
            win = Board.checkLine(column)
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
            win = Board.checkLine(diagonal)
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
            win = Board.checkLine(diagonal)
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
            win = Board.checkLine(diagonal)
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
            win = Board.checkLine(diagonal)
            if win != 0:
                return win

        if self.checkDraw():
            return -1

        # No result, game has not ended
        return 0

    def checkDraw(self):
        # Check draw
        full = True
        for y in range(15):
            for x in range(15):
                if self.pieces[y][x] == 0:
                    full = False
                    break
            if not full:
                break
        return full

    def checkWinPiece(self):
        # Return early if history is too short
        if len(self.history) < 9:
            return 0

        lastX, lastY = self.history[-1]

        # Horizontal
        start = max(0, lastX - 4)
        end = min(14, lastX + 4)
        line = [self.getPiece(i, lastY) for i in range(start, end + 1)]
        win = self.checkLine(line)
        if win != 0:
            return win

        # Vertical
        start = max(0, lastY - 4)
        end = min(14, lastY + 4)
        line = [self.getPiece(lastX, i) for i in range(start, end + 1)]
        win = self.checkLine(line)
        if win != 0:
            return win

        # Main diagonal
        startX = endX = lastX
        startY = endY = lastY
        while True:
            if lastX - startX == 4:
                # Travelled 4 pieces
                break
            if startX == 0 or startY == 0:
                # Reached edge
                break
            # Move down diagonal
            startX -= 1
            startY -= 1
        while True:
            if endX - lastX == 4:
                # Travelled 4 pieces
                break
            if endX == 14 or endY == 14:
                # Reached edge
                break
            # Move up diagonal
            endX += 1
            endY += 1

        rangeX = range(startX, endX + 1)
        rangeY = range(startY, endY + 1)
        # Combine ranges
        line = [self.getPiece(x, y) for x, y in zip(rangeX, rangeY)]
        win = self.checkLine(line)
        if win != 0:
            return win

        # Counter diagonal
        startX = endX = lastX
        startY = endY = lastY
        while True:
            if lastX - startX == 4:
                # Travelled 4 pieces
                break
            if startX == 0 or startY == 14:
                # Reached edge
                break
            # Move down diagonal
            startX -= 1
            startY += 1
        while True:
            if endX - lastX == 4:
                # Travelled 4 pieces
                break
            if endX == 14 or endY == 0:
                # Reached edge
                break
            # Move up diagonal
            endX += 1
            endY -= 1

        rangeX = range(startX, endX + 1)
        rangeY = range(startY, endY - 1, -1)
        # Combine ranges
        line = [self.getPiece(x, y) for x, y in zip(rangeX, rangeY)]
        win = self.checkLine(line)
        if win != 0:
            return win

        if self.checkDraw():
            return -1

        # No result, game has not ended
        return 0

    def getCurrentPlayer(self):
        return self.currentPlayer
