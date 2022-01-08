from src.model.presetsModel import PresetsTableModel, RespirationPresetsModel
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableView, QAbstractItemView, QPushButton


class PresetsTableView(QTableView):
    """
    This class is used to represent the respiration presets' data in a table view.
    """

    def __init__(self):
        super(PresetsTableView, self).__init__()

        # Set the TableView model
        self._presets_model = RespirationPresetsModel()
        self._table_model = PresetsTableModel(self._presets_model)
        self.setModel(self._table_model)

        # Make the user select only one whole row at a time
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.resizeRowsToContents()
        self.resizeColumnsToContents()


class PresetsViewWindow(QWidget):
    """
    Window for visualizing the respiration presets table including buttons for user interaction.
    """

    presets_table = PresetsTableView

    def __init__(self):
        super(PresetsViewWindow, self).__init__()
        self.setWindowTitle("Respiration Presets")
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
        self.send_preset_button.setText("Send Preset to Respirator")
        self.add_preset_button = QPushButton()
        self.add_preset_button.setText("Add new Preset")

        main_layout.addLayout(button_layout)
        button_layout.addWidget(self.add_preset_button)
        button_layout.addWidget(self.send_preset_button)
