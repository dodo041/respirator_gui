import logging
from random import randrange, uniform
from src.view.mainView import RespiratorMainWindow
from src.model.sensorDataModel import SensorDataModel


class MainController:
    """
    MainController handles the logic between model and view components.
    """

    _model = SensorDataModel
    _view = RespiratorMainWindow

    def __init__(self, sensor_model: SensorDataModel, view: RespiratorMainWindow):
        logging.debug("Creating new MVC main controller")
        self._model = sensor_model
        self._view = view
        self._connect_instrument_signals()

    def _connect_instrument_signals(self):
        logging.debug("Connecting PyQt signals to slots for instrument widgets")
        # Connect "modified data" signals to corresponding numerical instruments
        self._model.modified_animal_temp_data.connect(self._view.animal_temp_instrument.on_modified_data)
        self._model.modified_animal_temp_data.connect(self._view.animal_temp_graph.on_modified_data)

        self._model.modified_heatbed_temp_data.connect(self._view.heatbed_temp_instrument.on_modified_data)
        self._model.modified_heatbed_temp_data.connect(self._view.heatbed_temp_graph.on_modified_data)

        self._model.modified_air_temp_data.connect(self._view.air_temp_instrument.on_modified_data)
        self._model.modified_air_temp_data.connect(self._view.air_temp_graph.on_modified_data)

        self._model.modified_air_pressure_data.connect(self._view.pressure_inspiration_instrument.on_modified_data)
        self._model.modified_air_pressure_data.connect(self._view.pressure_inspiration_graph.on_modified_data)

        self._model.modified_eTVOC_data.connect(self._view.eTVOC_instrument.on_modified_data)
        self._model.modified_eTVOC_data.connect(self._view.eTVOC_graph.on_modified_data)

        self._model.modified_eCO2_data.connect(self._view.eCO2_instrument.on_modified_data)
        self._model.modified_eCO2_data.connect(self._view.eCO2_graph.on_modified_data)

        self._model.modified_relative_humidity_data.connect(self._view.relative_humidity_instrument.on_modified_data)
        self._model.modified_relative_humidity_data.connect(self._view.relative_humidity_graph.on_modified_data)

    def write_random_data(self):
        self._model.air_temp_data = uniform(29, 32)
        self._model.air_pressure_data = uniform(25, 30)
        self._model.animal_temp_data = randrange(37, 39, 1)
        self._model.heatbed_temp_data = randrange(35, 40, 1)
        self._model.eTVOC_data = randrange(150, 200, 1)
        self._model.eCO2_data = randrange(300, 500, 1)
        self._model.relative_humidity_data = randrange(80, 100, 1)
