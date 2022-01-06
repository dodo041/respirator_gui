from src.model.presetsModel import PresetsTableModel, RespirationPresetsModel
from PySide6.QtWidgets import QTableView, QAbstractItemView


class PresetsTableView(QTableView):

    def __init__(self):
        super(PresetsTableView, self).__init__()

        self.setWindowTitle("Respiration Presets")
        self.setMinimumSize(600, 200)

        # Set the TableView model
        self._presets_model = RespirationPresetsModel()
        self._table_model = PresetsTableModel(self._presets_model)
        self.setModel(self._table_model)

        # Make the user select only one whole row at a time
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.resizeRowsToContents()
        self.resizeColumnsToContents()
