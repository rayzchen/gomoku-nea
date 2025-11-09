# Local imports
from gomoku.colors import *
from gomoku.views.abc import InterfaceView
# Module imports
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QPainter, Qt, QBrush, QColor
from PySide6.QtCore import QPoint
import math

class BoardWidget(InterfaceView):
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
                self.board.playPiece(*self.cursorCell)
                self.processWin()
            self.update()

    def processWin(self):
        win = self.board.checkWinPiece()
        if win == 0:
            # No result
            return

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

        # Disable further input
        self.enableInput = False
        # Show box
        box.exec()

