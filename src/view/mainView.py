from src.view.instrumentView import NumericalInstrument, GraphInstrument
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QGridLayout, QMainWindow, QWidget, QMenuBar, QStatusBar


class RespiratorMainWindow(QMainWindow):
    """
    Main Window of the respirator GUI application.
    """

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
        self._build_instrument_view()

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

    def _build_instrument_view(self):
        """
        Builds the part of the main view containing the numerical instruments.
        """
        # TODO add translations
        # Create all numerical and graph instrument widgets
        self.animal_temp_instrument = NumericalInstrument("Temperatur Tier [°C]")
        self.animal_temp_graph = GraphInstrument()

        self.heatbed_temp_instrument = NumericalInstrument("Temperatur Heizplatte [°C]")
        self.heatbed_temp_graph = GraphInstrument()

        self.air_temp_instrument = NumericalInstrument("Temperatur Luft [°C]")
        self.air_temp_graph = GraphInstrument()

        self.pressure_inspiration_instrument = NumericalInstrument("Druck Inspirationskammer [psi]")
        self.pressure_inspiration_graph = GraphInstrument()

        self.eTVOC_instrument = NumericalInstrument("eTVOC [1]")
        self.eTVOC_graph = GraphInstrument()

        self.eCO2_instrument = NumericalInstrument("eCO2 [1]")
        self.eCO2_graph = GraphInstrument()

        self.relative_humidity_instrument = NumericalInstrument("Luftfeuchtigkeit [%]")
        self.relative_humidity_graph = GraphInstrument()

        # Set first two columns of instruments
        self.num_instruments_layout.addWidget(self.animal_temp_instrument, 0, 0)
        self.num_instruments_layout.addWidget(self.animal_temp_graph, 0, 1)

        self.num_instruments_layout.addWidget(self.heatbed_temp_instrument, 1, 0)
        self.num_instruments_layout.addWidget(self.heatbed_temp_graph, 1, 1)

        self.num_instruments_layout.addWidget(self.air_temp_instrument, 2, 0)
        self.num_instruments_layout.addWidget(self.air_temp_graph, 2, 1)

        self.num_instruments_layout.addWidget(self.pressure_inspiration_instrument, 3, 0)
        self.num_instruments_layout.addWidget(self.pressure_inspiration_graph, 3, 1)

        # Set second two column of instruments
        self.num_instruments_layout.addWidget(self.eTVOC_instrument, 0, 2)
        self.num_instruments_layout.addWidget(self.eTVOC_graph, 0, 3)

        self.num_instruments_layout.addWidget(self.eCO2_instrument, 1, 2)
        self.num_instruments_layout.addWidget(self.eCO2_graph, 1, 3)

        self.num_instruments_layout.addWidget(self.relative_humidity_instrument, 2, 2)
        self.num_instruments_layout.addWidget(self.relative_humidity_graph, 2, 3)
