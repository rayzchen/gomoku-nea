# Module imports
from PySide6.QtWidgets import QWidget, QApplication
from abc import ABCMeta, abstractmethod

class InterfaceView(QWidget, metaclass=ABCMeta):
    @abstractmethod
    def reset(self):
        # Must be overridden in subclass
        # (may be empty as well)
        pass

    def navigateTo(self, viewName):
        # Access current main window's methods
        window = QApplication.activeWindow()
        window.setView(viewName)
