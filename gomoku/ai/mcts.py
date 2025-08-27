import math
import random

# Get positions based on board size
BOARD_SIZE = 15
CENTRE = BOARD_SIZE * (BOARD_SIZE // 2) + BOARD_SIZE // 2

# Masks for shifting the board as a whole
leftmask = ~(sum(1 << (BOARD_SIZE*y) for y in range(BOARD_SIZE)))
rightmask = ~(sum(1 << (BOARD_SIZE*y+BOARD_SIZE-1) for y in range(BOARD_SIZE)))
left2mask = ~(sum(3 << (BOARD_SIZE*y) for y in range(BOARD_SIZE)))
right2mask = ~(sum(3 << (BOARD_SIZE*y+BOARD_SIZE-2) for y in range(BOARD_SIZE)))
fullmask = sum(1 << i for i in range(BOARD_SIZE*BOARD_SIZE))

class GomokuState:
    __slots__ = ["pieces1", "pieces2", "currentPlayer", "overallWinner", "legalMoves"]

    def __init__(self):
        self.pieces1 = 0
        self.pieces2 = 0
        self.currentPlayer = 1
        self.overallWinner = None
        self.calculateLegalMoves()

    def clone(self):
        # Do not call the constructor, only assign attributes
        clone = GomokuState.__new__(GomokuState)
        clone.pieces1 = self.pieces1
        clone.pieces2 = self.pieces2
        clone.currentPlayer = self.currentPlayer
        clone.overallWinner = self.overallWinner
        clone.legalMoves = self.legalMoves
        return clone

    def calculateLegalMoves(self):
        # Get all occupied positions
        occupied = self.pieces1 | self.pieces2
        if not occupied:
            self.legalMoves = 1 << CENTRE
            return

        # Get all positions in a 3x3 space around each piece
        shell = occupied >> BOARD_SIZE
        shell |= occupied << BOARD_SIZE
        shell |= (occupied & leftmask) >> 1
        shell |= (occupied & rightmask) << 1
        shell |= (occupied & leftmask) << (BOARD_SIZE-1)
        shell |= (occupied & rightmask) << (BOARD_SIZE+1)
        shell |= (occupied & leftmask) >> (BOARD_SIZE+1)
        shell |= (occupied & rightmask) >> (BOARD_SIZE-1)

        # Remove already occupied positions
        shell &= fullmask & ~occupied
        self.legalMoves = shell

    def checkPiecesWin(self, pieces):
        # Horizontal
        m = pieces & (pieces & rightmask) << 1
        m &= (m & right2mask) << 2
        if m & (m & rightmask) << 1:
            return True

        # Vertical
        m = pieces & pieces << BOARD_SIZE
        m &= m << (BOARD_SIZE*2)
        if m & m << BOARD_SIZE:
            return True

        # Main diagonal
        m = pieces & (pieces & rightmask) << (BOARD_SIZE+1)
        m &= (m & right2mask) << (BOARD_SIZE*2+2)
        if m & (m & rightmask) << (BOARD_SIZE+1):
            return True

        # Counter diagonal
        m = pieces & (pieces & leftmask) << (BOARD_SIZE-1)
        m &= (m & left2mask) << (BOARD_SIZE*2-2)
        if m & (m & leftmask) << (BOARD_SIZE-1):
            return True

        return False

    def checkWin(self):
        # Check each set of pieces separately
        if self.checkPiecesWin(self.pieces1):
            return 1
        elif self.checkPiecesWin(self.pieces2):
            return 2
        return 0

    def makeMove(self, move):
        # Flip a single bit
        if self.currentPlayer == 1:
            self.pieces1 |= 1 << move
        else:
            self.pieces2 |= 1 << move
        self.calculateLegalMoves()

        # Check win condition for either player
        win = self.checkWin()
        if win:
            self.overallWinner = win

        # Flip the current player
        self.currentPlayer = 3 - self.currentPlayer

    def isTerminal(self):
        return self.overallWinner is not None or self.legalMoves == 0

    def explore(self, moves=None):
        if moves is None:
            moves = self.legalMoves
        validMoves = [i for i in range(BOARD_SIZE*BOARD_SIZE) if moves & 1 << i]
        move = random.choice(validMoves)
        self.makeMove(move)
        return move

class MCTSNode:
    __slots__ = ["state", "parent", "move", "children", "untriedMoves", "visits", "wins", "lastPlayer"]

    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = {}
        self.untriedMoves = state.legalMoves
        self.visits = 0
        self.wins = 0
        self.lastPlayer = 1 if state.currentPlayer == 2 else 2

    def uctSelectChild(self, exploration=math.sqrt(2)):
        # Avoid log calculation for each child
        logN = math.log(self.visits)
        return max(
            self.children.values(),
            key=lambda c: (c.wins / c.visits) + exploration * math.sqrt(logN / c.visits)
        )

    def addChild(self, move, state):
        child = MCTSNode(state.clone(), parent=self, move=move)
        self.untriedMoves &= ~(1 << move)
        self.children[move] = child
        return child

    def update(self, result):
        self.visits += 1
        if result == self.lastPlayer:
            self.wins += 1

    def getNextNode(self, move):
        # Returns the root of a new tree
        # This node cannot be used anymore and should
        # be garbage collected
        if move in self.children:
            node = self.children[move]
            node.parent = None
        else:
            self.state.makeMove(move)
            node = MCTSNode(self.state)
        return node

def mcts(root, iterations):
    for i in range(iterations):
        node = root
        state = node.state.clone()

        # Selection
        while not node.untriedMoves and node.children:
            node = node.uctSelectChild()
            state.makeMove(node.move)

        # Expansion
        if node.untriedMoves:
            move = state.explore(node.untriedMoves)
            node = node.addChild(move, state)

        # Simulation
        while not state.isTerminal():
            state.explore()

        # Backpropagation
        result = state.overallWinner
        while node is not None:
            node.update(result)
            node = node.parent

    return max(root.children.values(), key=lambda c: c.visits).move
