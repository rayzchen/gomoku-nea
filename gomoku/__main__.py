# Local imports
from gomoku.gui import GomokuWindow
# Module imports
from PySide6.QtWidgets import QApplication
import sys

def main():
    # Pass command-line arguments to QApplication
    app = QApplication(sys.argv)

    # Create and show main window
    window = GomokuWindow()
    window.show()

    # Start event loop
    app.exec()

# Only create window if run as main entrypoint
if __name__ == "__main__":
    main()
