# Local imports
from gomoku.colors import *
from gomoku.views.abc import InterfaceView
from gomoku.views.game import BoardWidget
# Module imports
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QLabel, QFrame, QGridLayout, QPushButton, QListWidget, QSpacerItem, QSizePolicy, QListWidgetItem
from PySide6.QtGui import QFont, Qt
from PySide6.QtCore import Slot, QTimer, QElapsedTimer

class GameBrowser(InterfaceView):
    def __init__(self, board):
        # Attributes stored in sidebar
        self.player1Name = "player1"
        self.player2Name = "player2"
        self.player1Rating = "N/A"
        self.player2Rating = "N/A"

        # Timers for each player
        self.playerTimer1 = 300
        self.playerTimer2 = 300
        self.elapsedTimer = QElapsedTimer()
        self.elapsedTimer.start()

        self.timerRunning = True
        self.updateTimer = QTimer()
        self.updateTimer.setInterval(100)
        self.updateTimer.timeout.connect(self.updateTimerText)
        self.updateTimer.start()

        # Constants for the fonts used in the sidebar
        TITLE_TIMER_FONT = QFont("Noto Sans JP", 16)
        USERNAME_FONT = QFont("Noto Sans JP", 14)
        RATING_FONT = QFont("Noto Sans JP", 8)
        BUTTON_HISTORY_FONT = QFont("Noto Sans JP", 12)

        # Set up widget and layout
        super(InterfaceView, self).__init__()
        self.hlayout = QHBoxLayout()
        self.setLayout(self.hlayout)
        self.hlayout.setContentsMargins(0, 0, 0, 0)

        # Add board widget to layout
        self.board = board
        self.boardWidget = BoardWidget(self.board)
        self.hlayout.addWidget(self.boardWidget, 0)
        self.boardWidget.setFixedSize(600, 600)

        # Create sidebar
        self.sidebar = QWidget()
        self.vlayout = QVBoxLayout()
        self.sidebar.setLayout(self.vlayout)
        self.hlayout.addWidget(self.sidebar, 1)

        # Add players title
        self.title1 = QLabel("Players")
        self.vlayout.addWidget(self.title1)
        self.title1.setFont(TITLE_TIMER_FONT)
        self.title1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Make frame for player info
        self.playerFrame = QFrame()
        self.vlayout.addWidget(self.playerFrame)
        self.playerFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.playerFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.playergrid = QGridLayout()
        self.playerFrame.setLayout(self.playergrid)

        # Add player info rows
        self.player1 = QLabel()
        self.playergrid.addWidget(self.player1, 0, 0)
        self.player1.setFont(USERNAME_FONT)
        self.player2 = QLabel()
        self.playergrid.addWidget(self.player2, 0, 1)
        self.player2.setFont(USERNAME_FONT)

        self.rating1 = QLabel()
        self.playergrid.addWidget(self.rating1, 1, 0)
        self.rating1.setFont(RATING_FONT)
        self.rating2 = QLabel()
        self.playergrid.addWidget(self.rating2, 1, 1)
        self.rating2.setFont(RATING_FONT)

        self.timer1 = QLabel()
        self.playergrid.addWidget(self.timer1, 2, 0)
        self.timer1.setFont(TITLE_TIMER_FONT)
        self.timer2 = QLabel()
        self.playergrid.addWidget(self.timer2, 2, 1)
        self.timer2.setFont(TITLE_TIMER_FONT)

        # Add options title
        self.title2 = QLabel("Options")
        self.vlayout.addWidget(self.title2)
        self.title2.setFont(TITLE_TIMER_FONT)
        self.title2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add buttons in a row
        self.buttonlayout = QHBoxLayout()
        self.vlayout.addLayout(self.buttonlayout)
        self.buttonlayout.setSpacing(0)

        self.undo = QPushButton("Undo")
        self.buttonlayout.addWidget(self.undo)
        self.undo.setFont(BUTTON_HISTORY_FONT)
        self.draw = QPushButton("Draw")
        self.buttonlayout.addWidget(self.draw)
        self.draw.setFont(BUTTON_HISTORY_FONT)
        self.resign = QPushButton("Resign")
        self.buttonlayout.addWidget(self.resign)
        self.resign.setFont(BUTTON_HISTORY_FONT)

        # Add move history title
        self.title3 = QLabel("Move history")
        self.vlayout.addWidget(self.title3)
        self.title3.setFont(TITLE_TIMER_FONT)
        self.title3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.history = QListWidget()
        self.vlayout.addWidget(self.history)
        self.history.setFont(BUTTON_HISTORY_FONT)

        # Create spacers
        for position, height in [(0, 40), (3, 20), (6, 20), (9, 40)]:
            item = QSpacerItem(
                20, height,
                QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
            self.vlayout.insertSpacerItem(position, item)

        # Make history stretch
        self.vlayout.setStretch(8, 1)

        # Connect board widget signals to sidebar updating slots
        self.boardWidget.playerPlayed1.connect(self.changePlayer)
        self.boardWidget.playerPlayed2.connect(self.changePlayer)

        # Set initial label text
        self.updateLabels()

    def updateLabels(self):
        # Set username labels with current player marker
        player1Text = f"Black:\n{self.player1Name}"
        player2Text = f"White:\n{self.player2Name}"
        if self.board.getCurrentPlayer() == 1:
            player1Text += " 🡐"
        else:
            player2Text += " 🡐"
        self.player1.setText(player1Text)
        self.player2.setText(player2Text)

        # Set rating labels
        self.rating1.setText(f"Rating: {self.player1Rating}")
        self.rating2.setText(f"Rating: {self.player2Rating}")

    @Slot(int, int)
    def changePlayer(self, x, y):
        self.updateLabels()
        if self.board.getCurrentPlayer() == 2:
            # Black played piece
            name = self.player1Name
        else:
            # White played piece
            name = self.player2Name

        # Convert (0, 0) into a1
        pos = chr(x + 97) + str(y + 1)

        # Add entry to move history
        item = QListWidgetItem(f"{name} played {pos}")
        self.history.addItem(item)
        self.history.scrollToBottom()
        self.history.clearSelection()

        # Update player timers
        if self.timerRunning:
            if self.board.getCurrentPlayer() == 2:
                self.playerTimer1 -= self.elapsedTimer.restart() / 1000
            else:
                self.playerTimer2 -= self.elapsedTimer.restart() / 1000

    def updateTimerText(self):
        if self.board.getCurrentPlayer() == 1:
            time = self.playerTimer1 - self.elapsedTimer.elapsed() / 1000
            self.timer1.setText(self.formatTimer(time))
            self.timer2.setText(self.formatTimer(self.playerTimer2))
        else:
            time = self.playerTimer2 - self.elapsedTimer.elapsed() / 1000
            self.timer1.setText(self.formatTimer(self.playerTimer1))
            self.timer2.setText(self.formatTimer(time))

    def formatTimer(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:>02}:{seconds:>02}"
