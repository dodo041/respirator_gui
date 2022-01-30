from PySide6.QtCore import QSize, Slot
from PySide6.QtWidgets import QLCDNumber, QLabel, QVBoxLayout, QWidget, QSizePolicy


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

    @Slot(float)
    def on_modified_data(self, value: float) -> None:
        """
        Update value on LCD display.

        :param value: Data emitted from signal
        :return: None
        """
        self._lcd.display(value)
