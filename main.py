import sys
import logging
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from src.view.mainView import RespiratorMainWindow
from src.view.presetsView import PresetsViewWindow
from src.model.sensorDataModel import SensorDataModel
from src.controller.mainController import MainController

# Configure logging globally
log_path = "assets/logs.log"
log_fmt = "[{asctime},{msecs:3f}] {levelname} ({module}): {message}"
date_fmt = "%d.%m.%Y %H:%M:%S"
console_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler(filename=log_path)
logging.basicConfig(format=log_fmt, datefmt=date_fmt, handlers=[console_handler, file_handler], style="{")

logger = logging.getLogger()
logger.setLevel(logging.INFO)
if __debug__:
    logger.setLevel(logging.DEBUG)

logger.info("\n-------------- New session started --------------")

logger.debug("Creating sensor data model")
model = SensorDataModel()

if __name__ == "__main__":

    logger.debug("Creating PyQt application")
    app = QApplication(sys.argv)

    main_window = RespiratorMainWindow()
    main_window.show()

    p = PresetsViewWindow()

    main_window.open_presets_action.triggered.connect(p.show)
    logger.debug("Loading main MVC controller")
    mc = MainController(model, main_window)

    timer = QTimer()
    timer.setInterval(800)
    timer.timeout.connect(mc.write_random_data)

    while 1:
        logger.info("Running application main loop")
        timer.start()
        sys.exit(app.exec())
