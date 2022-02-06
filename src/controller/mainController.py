import logging
from random import randrange, uniform
from src.view.mainView import RespiratorMainWindow
from src.view.presetsView import PresetsViewWindow
from src.model.sensorDataModel import SensorDataModel
from src.controller.usbController import PicoUSBController


class MainController:
    """
    MainController handles the logic between model and view components. The model and view components as well as the
    USBController are instantiated when the MainController is instantiated.
    """

    _sensor_model = SensorDataModel
    _main_view = RespiratorMainWindow
    _presets_view = PresetsViewWindow
    _usb_controller = PicoUSBController

    def __init__(self):
        logging.debug("Creating new MVC main controller")

        # Models
        self._sensor_model = SensorDataModel()
        # Views
        self._main_view = RespiratorMainWindow()
        self._presets_view = PresetsViewWindow()
        # Additional controllers
        self._usb_controller = PicoUSBController()

        self._main_view.show()

        # Connect PyQt Signals to Slots
        self._connect_instrument_signals()
        self._connect_menu_actions()
        self._connect_presets_view_actions()

    """
    Methods for connecting PyQt signals and slots
    """

    def _connect_instrument_signals(self) -> None:
        logging.debug("Connecting PyQt signals to slots for instrument widgets")
        # Connect "modified data" signals to corresponding numerical instruments
        self._sensor_model.modified_animal_temp_data.connect(self._main_view.animal_temp_instrument.on_modified_data)
        self._sensor_model.modified_animal_temp_data.connect(self._main_view.animal_temp_graph.on_modified_data)

        self._sensor_model.modified_heatbed_temp_data.connect(self._main_view.heatbed_temp_instrument.on_modified_data)
        self._sensor_model.modified_heatbed_temp_data.connect(self._main_view.heatbed_temp_graph.on_modified_data)

        self._sensor_model.modified_air_temp_data.connect(self._main_view.air_temp_instrument.on_modified_data)
        self._sensor_model.modified_air_temp_data.connect(self._main_view.air_temp_graph.on_modified_data)

        self._sensor_model.modified_air_pressure_data.connect(self._main_view.pressure_inspiration_instrument.on_modified_data)
        self._sensor_model.modified_air_pressure_data.connect(self._main_view.pressure_inspiration_graph.on_modified_data)

        self._sensor_model.modified_eTVOC_data.connect(self._main_view.eTVOC_instrument.on_modified_data)
        self._sensor_model.modified_eTVOC_data.connect(self._main_view.eTVOC_graph.on_modified_data)

        self._sensor_model.modified_eCO2_data.connect(self._main_view.eCO2_instrument.on_modified_data)
        self._sensor_model.modified_eCO2_data.connect(self._main_view.eCO2_graph.on_modified_data)

        self._sensor_model.modified_relative_humidity_data.connect(self._main_view.relative_humidity_instrument.on_modified_data)
        self._sensor_model.modified_relative_humidity_data.connect(self._main_view.relative_humidity_graph.on_modified_data)

    def _connect_menu_actions(self) -> None:
        logging.debug("Connecting PyQt signals to slots for menu actions")
        self._main_view.open_presets_action.triggered.connect(self._presets_view.show)

    def _connect_presets_view_actions(self) -> None:
        logging.debug("Connecting PyQt signals to slots for presets view actions")
        self._presets_view.send_preset_button.clicked.connect(self.send_preset_to_pico)

        # Connect signal which gets emitted when a presets table row is selected
        self._presets_view.presets_table.selectionModel().selectionChanged.connect(self._presets_view.presets_table.get_table_row_data)

    """
    Methods for managing data and communication with Raspberry Pi Pico
    """

    def send_preset_to_pico(self) -> bool:
        """
        Send selected preset to Raspberry Pi Pico when "Send presets" button in the PresetsView is clicked.

        :return: Success of sending the selected preset to the Raspberry Pi Pico.
        """
        data = self._presets_view.presets_table.get_table_row_data()
        data_str = ""
        for key in data:
            data_str += data[key] + "\\ "
        # TODO add some char sequence to beginning of the data for check in Pico, if necessary
        data_bytes = data_str.encode()
        success = self._usb_controller.write_to_pico(data_bytes)
        # TODO check for ACK signal (some char sequence) to confirm that Pico indeed successfully got the data
        return success

    def write_random_data(self):
        self._sensor_model.air_temp_data = uniform(29, 32)
        self._sensor_model.air_pressure_data = uniform(25, 30)
        self._sensor_model.animal_temp_data = randrange(37, 39, 1)
        self._sensor_model.heatbed_temp_data = randrange(35, 40, 1)
        self._sensor_model.eTVOC_data = randrange(150, 200, 1)
        self._sensor_model.eCO2_data = randrange(300, 500, 1)
        self._sensor_model.relative_humidity_data = randrange(80, 100, 1)
