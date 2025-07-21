# Module imports
from PySide6.QtWidgets import QMainWindow

class GomokuWindow(QMainWindow):
    def __init__(self):
        super(GomokuWindow, self).__init__()
        # Make window unresizable
        self.setFixedSize(960, 600)
        self.setWindowTitle("GomokuNEA")
