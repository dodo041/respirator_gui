from src.view.instrumentView import NumericalInstrument
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QGridLayout, QLabel, QMainWindow, QWidget, QMenuBar, QStatusBar


class RespiratorMainWindow(QMainWindow):

    menu_bar = QMenuBar
    status_bar = QStatusBar

    animal_temp_instrument = NumericalInstrument
    heatbed_temp_instrument = NumericalInstrument
    air_temp_instrument = NumericalInstrument
    pressure_inspiration_instrument = NumericalInstrument
    eTVOC_instrument = NumericalInstrument
    eCO2_instrument = NumericalInstrument
    relative_humidity_instrument = NumericalInstrument

    def __init__(self):
        super(RespiratorMainWindow, self).__init__()
        self.setWindowTitle("Ventilator GUI")
        self.setMinimumSize(1000, 600)

        # Create main container (widget) containing the numerical instruments
        self.num_instruments_container = QWidget(self)
        self.setCentralWidget(self.num_instruments_container)
        # Grid layout to nicely place the numerical instruments inside the main container
        self.num_instruments_layout = QGridLayout()
        self.num_instruments_layout.setSpacing(0)
        self.num_instruments_container.setLayout(self.num_instruments_layout)

        self._build_menu_bar()
        self._build_status_bar()
        self._build_numerical_instrument_view()

    def _build_menu_bar(self):
        """
        Builds the top menu bar for accessing different functional parts of the GUI.
        """
        self.menu_bar = QMenuBar()
        self.setMenuBar(self.menu_bar)
        # TODO add translations
        # Mark ALT key shortcuts with an "&" sign
        tools_menu = self.menu_bar.addMenu("&Einstellungen")
        self.open_presets_action = QAction("Beatmungs-&Voreinstellungen...")
        tools_menu.addAction(self.open_presets_action)

    def _build_status_bar(self):
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("Respirator <status>")
        self.setStatusBar(self.status_bar)

    def _build_numerical_instrument_view(self):
        """
        Builds the part of the main view containing the numerical instruments.
        """
        # TODO add translations
        self.animal_temp_instrument = NumericalInstrument("Temperatur Tier [°C]")
        self.heatbed_temp_instrument = NumericalInstrument("Temperatur Heizplatte [°C]")
        self.air_temp_instrument = NumericalInstrument("Temperatur Luft [°C]")
        self.pressure_inspiration_instrument = NumericalInstrument("Druck Inspirationskammer [psi]")
        self.eTVOC_instrument = NumericalInstrument("eTVOC [1]")
        self.eCO2_instrument = NumericalInstrument("eCO2 [1]")
        self.relative_humidity_instrument = NumericalInstrument("Luftfeuchtigkeit [%]")

        # First (instrument) column
        self.num_instruments_layout.addWidget(QLabel("Temperatur"), 0, 0)
        self.num_instruments_layout.addWidget(self.animal_temp_instrument, 1, 0)
        self.num_instruments_layout.addWidget(self.heatbed_temp_instrument, 2, 0)
        self.num_instruments_layout.addWidget(self.air_temp_instrument, 3, 0)
        # Third (instrument) column
        self.num_instruments_layout.addWidget(QLabel("Luftqualität"), 0, 1)
        self.num_instruments_layout.addWidget(self.eTVOC_instrument, 1, 1)
        self.num_instruments_layout.addWidget(self.eCO2_instrument, 2, 1)
        self.num_instruments_layout.addWidget(self.relative_humidity_instrument, 3, 1)
        # Fifth (instrument) column
        self.num_instruments_layout.addWidget(QLabel("Druck"), 0, 2)
        self.num_instruments_layout.addWidget(self.pressure_inspiration_instrument, 1, 2)

        # Set stretch factors to account for different widget sizes in the grid cells
        # self.numericalInstrumentsLayout.setRowStretch(0, 0)
        self.num_instruments_layout.setRowStretch(1, 1)
        self.num_instruments_layout.setRowStretch(2, 1)
        self.num_instruments_layout.setRowStretch(3, 1)
        self.num_instruments_layout.setColumnStretch(0, 1)
        self.num_instruments_layout.setColumnStretch(1, 1)
        self.num_instruments_layout.setColumnStretch(2, 1)
