import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from src.view.mainView import RespiratorMainWindow
from src.view.presetsView import PresetsViewWindow
from src.model.sensorDataModel import SensorDataModel
from src.controller.mainController import MainController

model = SensorDataModel()

if __name__ == "__main__":

    app = QApplication(sys.argv)

    main_window = RespiratorMainWindow()
    main_window.show()

    p = PresetsViewWindow()

    main_window.open_presets_action.triggered.connect(p.show)

    mc = MainController(model, main_window)

    timer = QTimer()
    timer.setInterval(800)
    timer.timeout.connect(mc.write_random_data)

    while 1:
        timer.start()
        sys.exit(app.exec())
