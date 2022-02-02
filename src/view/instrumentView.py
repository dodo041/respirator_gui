import time
from collections import deque
from PySide6.QtCore import QSize, Slot
from PySide6.QtWidgets import QLCDNumber, QLabel, QVBoxLayout, QWidget, QSizePolicy
from pyqtgraph import PlotWidget, PlotItem, PlotDataItem, DateAxisItem


class NumericalInstrument(QWidget):
    """
    Instrument widget which displays numerical values in LCD display style with a text label.
    """

    _min_width = 200
    _decimal_places = 5
    _lcd = QLCDNumber
    _instrument_title = str

    def __init__(self, instrument_label: str):
        super(NumericalInstrument, self).__init__()
        self._build_numerical_instrument(instrument_label)

        # Set border around widget and inner elements as visual hint during debugging
        if __debug__:
            self.setStyleSheet("border: 1px solid blue;")
            self._lcd.setStyleSheet("border: 1px solid red;")
            self._instrument_title.setStyleSheet("border: 1px solid green;")

    def _build_numerical_instrument(self, instrument_label: str) -> None:
        """
        Build a numerical LCD instrument.

        :param instrument_label: Description to be displayed
        :return: None
        """
        # Wrapper for inner contents of the NumericalInstrument (might be handy for later extension)
        wrap_layout = QVBoxLayout(self)
        wrap = QWidget()
        wrap_layout.addWidget(wrap)
        # Inner layout with actual contents
        inner_layout = QVBoxLayout(wrap)

        self._instrument_title = QLabel(instrument_label)
        self._lcd = QLCDNumber(self._decimal_places)
        # Configure LCD widget
        self._lcd.setSegmentStyle(self._lcd.Flat)
        self._lcd.setSmallDecimalPoint(True)

        inner_layout.addWidget(self._lcd)
        inner_layout.addWidget(self._instrument_title)

        self._set_size_policies()

    def sizeHint(self) -> QSize:
        """
        Reimplementation of PyQt sizeHint.

        :return: Preferred size of the NumericalInstrument widget.
        """
        return QSize(self._min_width, int(self._min_width * 0.6))

    def _set_size_policies(self) -> None:
        """
        Set the PyQt size policies for the NumericalInstrument widget.

        :return: None
        """
        # LCD display shall expand as much as possible in vertical direction
        lcd_sp = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        self._lcd.setSizePolicy(lcd_sp)

        # NumericalInstrument widget and its contents shall not exceed the given size hint
        num_instr_sp = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.setSizePolicy(num_instr_sp)

    @Slot(deque)
    def on_modified_data(self, data: deque) -> None:
        """
        Update value on LCD display.

        :param data: Data as tuples of (value, datetime) to be displayed
        :return: None
        """
        # Get youngest (last) entry from sensor data deque and display the value in LCD
        value = data[-1][0]
        self._lcd.display(value)


class GraphInstrument(QWidget):
    """
    Instrument for displaying data as a graph in a cartesian coordinate system.
    """
    _MAX_VALUES = 120
    _min_height = 150
    _inner_layout = QVBoxLayout
    _plot_widget = PlotWidget
    _graph_data = PlotDataItem

    def __init__(self):
        super(GraphInstrument, self).__init__()
        self._build_graph_instrument()
        if __debug__:
            self.setStyleSheet("border: 1px solid blue;")

    def _build_graph_instrument(self) -> None:
        """
        Build the GraphInstrument. Doing this (and especially updating the graph afterwards) natively with PyQt is
        absolute pain, therefore it's done with pyqtgraph, which leaves us with softer pain.

        :return: None
        """
        # Native PyQt wrapper for inner contents of GraphInstrument (might be handy for later extension)
        wrap_layout = QVBoxLayout(self)
        wrap = QWidget()
        wrap_layout.addWidget(wrap)
        # Inner layout with actual contents
        self._inner_layout = QVBoxLayout(wrap)

        """
        For pyqtgraph plot structure consider https://pyqtgraph.readthedocs.io/en/latest/plotting.html
        """
        # x-axis shall display datetime information for each y-value
        x_axis = DateAxisItem()
        # The PlotDataItem contains and manages the actual data to be displayed
        self._graph_data = PlotDataItem(pen={"color": "#0088FF", "width": 1.5}, antialias=True)
        # The PlotItem contains all graph-related widgets (graph itself, axes, labels, etc.)
        _graph = PlotItem(axisItems={"bottom": x_axis}, enableMenu=False)
        _graph.showGrid(True, True, 0.4)
        _graph.addItem(self._graph_data)

        # pyqtgraph container for the graph which we can embed in our PyQt GUI
        _plot_widget = PlotWidget(background="#00000000", plotItem=_graph)  # Set background (#RRGGBBAA) transparent
        _plot_widget.setAntialiasing(True)
        _plot_widget.plotItem.setMouseEnabled(x=True, y=False)  # Allow zooming only along the x-axis

        self._inner_layout.addWidget(_plot_widget)

        # GraphInstrument should shall not exceed given size hint
        graph_instr_sp = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.setSizePolicy(graph_instr_sp)

    def sizeHint(self) -> QSize:
        """
        Reimplementation of PyQt sizeHint.

        :return: Preferred size of the GraphInstrument widget.
        """
        return QSize(self._min_height * 3, self._min_height)

    @Slot(deque)
    def on_modified_data(self, data: deque) -> None:
        """
        Update data to be displayed in GraphInstrument. Setting the data automatically redraws the graph.

        :param data: Data as tuple of (value, datetime) to be plotted in the GraphInstrument
        :return: None
        """
        times = []
        values = []

        # TODO room for optimization here: maybe taking the last N data points can be avoided by MAX_QUEUE_LENGTH in
        # the SensorDataModel, and just plotting all data + scaling axes might be faster than doing this, especially in
        # high throughput scenarios
        last_n = deque()
        index = -self._MAX_VALUES
        if len(data) > self._MAX_VALUES:
            for n in range(self._MAX_VALUES):
                last_n.append(data[index])
                index += 1
        else:
            last_n = data

        for data_point in last_n:
            values.append(data_point[0])
            times.append(time.mktime(data_point[1].timetuple()))

        self._graph_data.setData(x=times, y=values)
