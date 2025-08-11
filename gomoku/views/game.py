# Local imports
from gomoku.colors import *
from gomoku.views.abc import InterfaceView
# Module imports
from PySide6.QtWidgets import QVBoxLayout, QLabel
from PySide6.QtGui import QPainter, Qt, QBrush
from PySide6.QtCore import QPoint

class BoardWidget(InterfaceView):
    def __init__(self, board):
        # Set up widget and layout
        super(BoardWidget, self).__init__()
        self.vlayout = QVBoxLayout()
        self.setLayout(self.vlayout)
        self.vlayout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel()
        self.vlayout.addWidget(self.label)
        self.label.resize(600, 600)

        # Store reference to board state
        self.board = board

    def reset(self):
        pass

    def paintEvent(self, event):
        # Handle event and create painter object
        super(BoardWidget, self).paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setWindow(0, 0, 600, 600)

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

    def resizeEvent(self, event):
        # Ensure the dimensions of the widget remain square
        super(BoardWidget, self).resizeEvent(event)
        size = min(event.size().width(), event.size().height())
        self.resize(size, size)
