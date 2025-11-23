# Local imports
from gomoku.views.menu import MainMenuView
from gomoku.views.select import GameSelection
from gomoku.views.browser import GameBrowser
# Module imports
from PySide6.QtWidgets import QMainWindow

class GomokuWindow(QMainWindow):
    def __init__(self):
        super(GomokuWindow, self).__init__()
        # Make window unresizable
        self.setFixedSize(960, 600)
        self.setWindowTitle("GomokuNEA")

        # Lookup table of views
        self.views = {
            "menu": MainMenuView(),
            "select": GameSelection(),
            "game": GameBrowser(),
        }
        self.currentView = None

    def setView(self, name):
        # Check whether provided view exists
        if name not in self.views:
            raise Exception(f"Could not find view {name}")

        # Reset new view
        self.views[name].reset()

        # Replace main view
        self.setCentralWidget(self.views[name])
        self.currentView = name

    def getView(self, name):
        # Check whether provided view exists
        if name not in self.views:
            raise Exception(f"Could not find view {name}")

        # Return view with provided name
        return self.views[name]
