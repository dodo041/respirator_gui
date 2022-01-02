import sys
from PySide6.QtWidgets import QApplication
from src.view.mainView import RespiratorMainWindow


if __name__ == "__main__":

    app = QApplication(sys.argv)

    main_window = RespiratorMainWindow()
    main_window.show()

    sys.exit(app.exec())
