# Local imports
from gomoku.board import Board
from gomoku.views.abc import InterfaceView
from gomoku.views.game import BoardWidget, MCTSWorker
# Module imports
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QLabel, QGridLayout, QComboBox, QCheckBox, QPushButton, QSpacerItem, QSizePolicy
from PySide6.QtGui import QFont, Qt

class GameSelection(InterfaceView):
    def __init__(self):
        # Constants for the fonts used in the sidebar
        TITLE_FONT = QFont("Noto Sans JP", 24)
        TEXT_FONT = QFont("Noto Sans JP", 14)

        # Set up widget and layout
        super(InterfaceView, self).__init__()
        self.hlayout = QHBoxLayout()
        self.setLayout(self.hlayout)
        self.hlayout.setContentsMargins(0, 0, 0, 0)

        # Add empty board widget to layout
        self.boardWidget = BoardWidget(Board())
        self.hlayout.addWidget(self.boardWidget, 0)
        self.boardWidget.setFixedSize(600, 600)

        # Ensure board is not interactable
        self.boardWidget.enableInput = False

        # Create sidebar
        self.sidebar = QWidget()
        self.vlayout = QVBoxLayout()
        self.sidebar.setLayout(self.vlayout)
        self.hlayout.addWidget(self.sidebar, 1)

        # Add title
        self.title = QLabel("New Game")
        self.vlayout.addWidget(self.title)
        self.title.setFont(TITLE_FONT)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add selection grid
        self.gridlayout = QGridLayout()
        self.vlayout.addLayout(self.gridlayout)

        self.label1 = QLabel("Game duration")
        self.gridlayout.addWidget(self.label1, 0, 0)
        self.label1.setFont(TEXT_FONT)
        self.label2 = QLabel("Time increment")
        self.gridlayout.addWidget(self.label2, 1, 0)
        self.label2.setFont(TEXT_FONT)
        self.label3 = QLabel("Opening rules")
        self.gridlayout.addWidget(self.label3, 2, 0)
        self.label3.setFont(TEXT_FONT)
        self.label4 = QLabel("Rated?")
        self.gridlayout.addWidget(self.label4, 3, 0)
        self.label4.setFont(TEXT_FONT)
        self.label5 = QLabel("Player 1 AI")
        self.gridlayout.addWidget(self.label5, 4, 0)
        self.label5.setFont(TEXT_FONT)
        self.label6 = QLabel("Player 2 AI")
        self.gridlayout.addWidget(self.label6, 5, 0)
        self.label6.setFont(TEXT_FONT)

        self.combo1 = QComboBox()
        self.gridlayout.addWidget(self.combo1, 0, 1)
        self.combo1.setFont(TEXT_FONT)
        for duration in [1, 2, 3, 5, 10, 15]:
            if duration == 1:
                self.combo1.addItem("1 minute", duration * 60)
            else:
                self.combo1.addItem(f"{duration} minutes", duration * 60)
        self.combo1.setCurrentText("5 minutes")

        self.combo2 = QComboBox()
        self.gridlayout.addWidget(self.combo2, 1, 1)
        self.combo2.setFont(TEXT_FONT)
        for duration in [0, 1, 10]:
            if duration == 1:
                self.combo2.addItem("1 second", duration)
            else:
                self.combo2.addItem(f"{duration} seconds", duration)
        self.combo1.setCurrentText("0 seconds")

        self.combo3 = QComboBox()
        self.gridlayout.addWidget(self.combo3, 2, 1)
        self.combo3.setFont(TEXT_FONT)
        for choice in ["None", "Swap", "Pro", "Swap2", "Renju"]:
            self.combo3.addItem(choice)
        self.combo1.setCurrentText("None")

        self.checkbox1 = QCheckBox()
        self.gridlayout.addWidget(self.checkbox1, 3, 1)
        self.checkbox2 = QCheckBox()
        self.gridlayout.addWidget(self.checkbox2, 4, 1)
        self.checkbox3 = QCheckBox()
        self.gridlayout.addWidget(self.checkbox3, 5, 1)

        # Add start button
        self.buttonlayout = QHBoxLayout()
        self.vlayout.addLayout(self.buttonlayout)
        self.start = QPushButton("Start game")
        self.buttonlayout.addWidget(self.start)
        self.start.setFont(TEXT_FONT)
        self.start.pressed.connect(self.startGame)

        # Create spacers
        for position in [0, 2, 4, 6]:
            # Vertically expanding
            item = QSpacerItem(
                20, 40,
                QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
            self.vlayout.insertSpacerItem(position, item)
        for position in [0, 2]:
            # Horizontally expanding
            item = QSpacerItem(
                20, 40,
                QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
            self.buttonlayout.insertSpacerItem(position, item)

        # Adjust layout stretches
        self.gridlayout.setColumnStretch(0, 1)
        self.vlayout.setStretch(0, 1)
        self.vlayout.setStretch(6, 1)
        self.buttonlayout.setStretch(0, 1)
        self.buttonlayout.setStretch(1, 2)
        self.buttonlayout.setStretch(2, 1)

    def startGame(self):
        # Set starting timers of players in GameBrowser view
        view = self.getView("game")
        view.playerTimer1 = self.combo1.currentData()
        view.playerTimer2 = self.combo1.currentData()

        # Add AI player workers when necessary
        if self.checkbox2.isChecked():
            view.boardWidget.assignWorker(MCTSWorker(), 1)
        if self.checkbox3.isChecked():
            view.boardWidget.assignWorker(MCTSWorker(), 2)

        # Change the current view
        self.navigateTo("game")
