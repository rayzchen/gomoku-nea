# Local imports
from gomoku.colors import *
from gomoku.views.abc import InterfaceView
from gomoku.ai.mcts import GomokuState, MCTSNode, mcts
# Module imports
from PySide6.QtWidgets import QMessageBox, QApplication
from PySide6.QtGui import QPainter, Qt, QBrush, QColor
from PySide6.QtCore import QPoint, QObject, Signal, Slot, QThread, QTimer
import math

class BoardWidget(InterfaceView):
    playerPlayed1 = Signal(int, int)
    playerPlayed2 = Signal(int, int)
    requestMove1 = Signal()
    requestMove2 = Signal()

    def __init__(self, board):
        # Set up widget
        super(BoardWidget, self).__init__()

        # Store reference to board state
        self.board = board

        # Store location that mouse pointer points to
        # None if pointer is not in board
        self.cursorCell = None
        # Make sure this widget can access pointer location
        self.setMouseTracking(True)

        # Toggle mouse input
        self.enableInput = True

        # Store reference to workers
        self.workers = {1: None, 2: None}
        self.gameEnd = False

    def assignWorker(self, worker, number):
        worker.finished.connect(self.playPiece)
        self.workers[number] = worker

        if number == 1:
            self.playerPlayed1.connect(worker.processMove)
            self.requestMove1.connect(worker.getMove)
        else:
            self.playerPlayed2.connect(worker.processMove)
            self.requestMove2.connect(worker.getMove)

    def reset(self):
        self.cursorCell = None
        self.enableInput = True

    def paintEvent(self, event):
        # Handle event and create painter object
        super(BoardWidget, self).paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setWindow(0, 0, 600, 600)

        size = min(self.width(), self.height())
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        painter.setViewport(x, y, size, size)

        self.drawBoard(painter)
        if self.enableInput:
            self.drawCursor(painter)

    def drawBoard(self, painter):
        # Draw background
        painter.fillRect(0, 0, 600, 600, BACKGROUND_COLOR)

        # Draw grid
        painter.setPen(BOARD_LINE_COLOR)
        for x in range(16):
            painter.drawLine(20 + x * 40, 20, 20 + x * 40, 580)
        for y in range(16):
            painter.drawLine(20, 20 + y * 40, 580, 20 + y * 40)
        painter.setPen(Qt.PenStyle.NoPen)

        # Draw board embellishments
        painter.setBrush(QBrush(BOARD_LINE_COLOR))
        painter.drawEllipse(QPoint(140, 140), 4, 4)
        painter.drawEllipse(QPoint(460, 140), 4, 4)
        painter.drawEllipse(QPoint(140, 460), 4, 4)
        painter.drawEllipse(QPoint(460, 460), 4, 4)
        painter.drawEllipse(QPoint(300, 300), 4, 4)

        # Draw pieces
        for y in range(15):
            for x in range(15):
                piece = self.board.getPiece(x, y)
                if piece == 1:
                    painter.setBrush(QBrush(BLACK_PIECE_COLOR))
                elif piece == 2:
                    painter.setBrush(QBrush(WHITE_PIECE_COLOR))
                else:
                    continue

                # Qt coordinate system has (0, 0) at top left
                pos = QPoint(20 + x*40, 600 - (20 + y*40))
                painter.drawEllipse(pos, 15, 15)

    def drawCursor(self, painter):
        # Draw cursor piece (if possible)
        if self.cursorCell is not None:
            x, y = self.cursorCell
            if self.board.positionEmpty(x, y):
                if self.board.currentPlayer == 1:
                    color = QColor(BLACK_PIECE_COLOR)
                else:
                    color = QColor(WHITE_PIECE_COLOR)
                color.setAlpha(128)

                painter.setBrush(QBrush(color))
                pos = QPoint(20 + x*40, 600 - (20 + y*40))
                painter.drawEllipse(pos, 15, 15)

    def resizeEvent(self, event):
        # Ensure the dimensions of the widget remain square
        super(BoardWidget, self).resizeEvent(event)
        size = min(event.size().width(), event.size().height())
        self.resize(size, size)

    def mouseMoveEvent(self, event):
        # Store the position of the cell that the mouse is hovering over
        super(BoardWidget, self).mouseMoveEvent(event)
        pos = event.position()
        cellSize = self.width() / 15
        self.cursorCell = (
            math.floor(pos.x() / cellSize),
            math.floor(15 - pos.y() / cellSize)
        )
        if self.cursorCell[0] < 0 or self.cursorCell[0] > 14:
            self.cursorCell = None
        elif self.cursorCell[1] < 0 or self.cursorCell[1] > 14:
            self.cursorCell = None
        self.update()

    def leaveEvent(self, event):
        # Reset the hovered cell
        super(BoardWidget, self).leaveEvent(event)
        self.cursorCell = None
        self.update()

    def mouseReleaseEvent(self, event):
        super(BoardWidget, self).mouseReleaseEvent(event)
        if self.enableInput and event.button() == Qt.MouseButton.LeftButton:
            if self.board.positionEmpty(*self.cursorCell):
                self.playPiece(*self.cursorCell)

    @Slot(int, int)
    def playPiece(self, x, y):
        self.board.playPiece(x, y)
        self.update()

        currentPlayer = self.board.getCurrentPlayer()
        if currentPlayer == 1:
            self.playerPlayed1.emit(x, y)
        elif currentPlayer == 2:
            self.playerPlayed2.emit(x, y)

        self.processWin()
        if self.gameEnd:
            return
        if currentPlayer == 1:
            self.requestMove1.emit()
        elif currentPlayer == 2:
            self.requestMove2.emit()

        if self.workers[currentPlayer] is not None:
            self.enableInput = False
        else:
            self.enableInput = True

    def processWin(self):
        win = self.board.checkWinPiece()
        if win == 0:
            # No result
            return
        self.gameEnd = True
        self.enableInput = False

        # Create message box
        box = QMessageBox()
        box.setWindowTitle("Game result")

        # Select text
        if win == 1:
            box.setText("Player 1 has won!")
        elif win == 2:
            box.setText("Player 2 has won!")
        elif win == -1:
            box.setText("The game is a tie!")

        # Show box
        box.exec()

class WorkerBase(QObject):
    finished = Signal(int, int)

    def __init__(self):
        super(WorkerBase, self).__init__()
        self.workerThread = QThread()
        QApplication.instance().aboutToQuit.connect(self.cleanup)
        self.moveToThread(self.workerThread)
        self.workerThread.start()

    def cleanup(self):
        self.workerThread.terminate()
        self.workerThread.wait()

    def processMove(self, x, y):
        pass

    def getMove(self):
        pass

class MCTSWorker(WorkerBase):
    def __init__(self):
        super(MCTSWorker, self).__init__()
        self.node = MCTSNode(GomokuState())

    @Slot(int, int)
    def processMove(self, x, y):
        self.node = self.node.getNextNode(15*y+x)

    @Slot()
    def getMove(self):
        move = mcts(self.node, 2000)
        self.node = self.node.getNextNode(move)
        self.finished.emit(move % 15, move // 15)
