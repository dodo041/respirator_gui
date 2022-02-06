import logging
from src.model.presetsModel import PresetsTableModel, RespirationPresetsModel
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableView, QAbstractItemView, QPushButton


class PresetsTableView(QTableView):
    """
    This class is used to represent the respiration presets' data in a table view.
    """

    def __init__(self):
        logging.debug("Initialising presets table view")
        super(PresetsTableView, self).__init__()

        # Set the TableView model
        logging.debug("Setting PyQt TableView model from respiration presets model")
        self._presets_model = RespirationPresetsModel()
        self._table_model = PresetsTableModel(self._presets_model)
        self.setModel(self._table_model)

        # Make the user select only one whole row at a time
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.resizeRowsToContents()
        self.resizeColumnsToContents()

    def get_table_row_data(self) -> {}:
        """
        Retrieve the data of the currently selected table row directly from the native RespirationPresetsModel.

        :return: Table row data (dict style).
        """
        data = {}
        selected_row_index = self.currentIndex().row()
        # Get the key/name of the selected preset using the row index
        preset = list(self._presets_model.presets.sections())[selected_row_index]

        # Loop through all presets values (options)
        for preset_value in self._presets_model.presets.options(preset):
            data[preset_value] = self._presets_model.presets.get(preset, preset_value)
        logging.debug(f"Selected preset '{preset}' ({selected_row_index + 1}. row) with data {data}")
        return data


class PresetsViewWindow(QWidget):
    """
    Window for visualizing the respiration presets table including buttons for user interaction.
    """
    # TODO add translations
    presets_table = PresetsTableView

    def __init__(self):
        logging.debug("Initialising presets view window")
        super(PresetsViewWindow, self).__init__()
        self.setWindowTitle("Beatmungs-Voreinstellungen")
        self.setMinimumSize(600, 200)

        self._build_presets_view_window()

    def _build_presets_view_window(self):
        self.presets_table = PresetsTableView()
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        # Add table to main_layout layout before adding button_layout to it, so that table is displayed above buttons
        self.setLayout(main_layout)
        main_layout.addWidget(self.presets_table)

        # Buttons for handling presets
        self.send_preset_button = QPushButton()
        self.send_preset_button.setText("Voreinstellung an Beatmungsgerät senden")
        self.add_preset_button = QPushButton()
        self.add_preset_button.setText("Neue Voreinstellung erstellen")

        main_layout.addLayout(button_layout)
        button_layout.addWidget(self.add_preset_button)
        button_layout.addWidget(self.send_preset_button)
