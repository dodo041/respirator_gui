import sys
from random import randrange, uniform
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from src.view.mainView import RespiratorMainWindow
from src.view.presetsView import PresetsTableView
from src.model.sensorDataModel import SensorDataModel

model = SensorDataModel()


def write_random():
    model.write_air_temp_data(uniform(29, 32))
    model.write_air_pressure_data(uniform(25, 30))
    model.write_animal_temp_data(randrange(37, 39, 1))
    model.write_heatbed_temp_data(randrange(35, 40, 1))
    model.write_eTVOC_data(randrange(150, 200, 1))
    model.write_eCO2_data(randrange(300, 500, 1))
    model.write_relative_humidity_data(randrange(80, 100, 1))


if __name__ == "__main__":

    app = QApplication(sys.argv)

    main_window = RespiratorMainWindow()
    main_window.show()

    p = PresetsTableView()
    p.show()

    model.modified_air_temp_data.connect(main_window.air_temp_instrument.on_modified_data)
    model.modified_air_pressure_data.connect(main_window.pressure_inspiration_instrument.on_modified_data)
    model.modified_animal_temp_data.connect(main_window.animal_temp_instrument.on_modified_data)
    model.modified_heatbed_temp_data.connect(main_window.heatbed_temp_instrument.on_modified_data)
    model.modified_eTVOC_data.connect(main_window.eTVOC_instrument.on_modified_data)
    model.modified_eCO2_data.connect(main_window.eCO2_instrument.on_modified_data)
    model.modified_relative_humidity_data.connect(main_window.relative_humidity_instrument.on_modified_data)

    timer = QTimer()
    timer.setInterval(800)
    timer.timeout.connect(write_random)

    while 1:
        timer.start()
        sys.exit(app.exec())
