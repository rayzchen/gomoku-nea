# Local imports
from gomoku.views.abc import InterfaceView
# Module imports
from PySide6.QtWidgets import QVBoxLayout, QSpacerItem, QLabel, QHBoxLayout, QPushButton, QSizePolicy
from PySide6.QtGui import QFont, Qt

class MainMenuView(InterfaceView):
    def __init__(self):
        # Constants for the fonts used in the menu
        TITLE_FONT = QFont("Noto Sans JP", 60)
        BUTTON_FONT = QFont("Noto Sans JP", 16)

        # Set up widget and layout
        super(MainMenuView, self).__init__()
        self.vlayout = QVBoxLayout()
        self.setLayout(self.vlayout)

        # Create and position title label
        self.title = QLabel("GomokuNEA")
        self.vlayout.addWidget(self.title)
        self.title.setFont(TITLE_FONT)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # More layouts for buttons
        self.hlayout = QHBoxLayout()
        self.vlayout.addLayout(self.hlayout)
        self.buttonLayout = QVBoxLayout()
        self.hlayout.addLayout(self.buttonLayout)

        # Create buttons
        buttons = []
        for label in ["Play game", "Profile", "Game browser", "Settings", "Quit"]:
            button = QPushButton(label)
            self.buttonLayout.addWidget(button)
            button.setFont(BUTTON_FONT)
            button.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            buttons.append(button)

        # Create spacers
        for position in [0, 2, 4]:
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
            self.hlayout.insertSpacerItem(position, item)

        # Adjust layout stretches
        self.vlayout.setStretch(0, 1)
        self.vlayout.setStretch(1, 2)
        self.vlayout.setStretch(2, 1)
        self.vlayout.setStretch(3, 5)
        self.vlayout.setStretch(4, 1)

        self.hlayout.setStretch(0, 1)
        self.hlayout.setStretch(1, 2)
        self.hlayout.setStretch(2, 1)

    def reset(self):
        # Method is required but has no functionality
        pass
