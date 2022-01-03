from PySide6.QtCore import QSize, Slot
from PySide6.QtWidgets import QLCDNumber, QLabel, QVBoxLayout, QWidget


class NumericalInstrument(QWidget):
    """
    Instrument widget which displays numerical values in LCD display style with a text label.
    """

    _instrument_size = QSize(200, 100)
    _decimal_places = 5
    _value = 0
    lcd = QLCDNumber

    def __init__(self, instrumentLabel: str):
        super(NumericalInstrument, self).__init__()
        self._build_numerical_instrument(instrumentLabel)

    def _build_numerical_instrument(self, instrumentLabel: str) -> None:
        """
        Build a numerical LCD instrument.

        :param instrumentLabel: Description to be displayed
        :return: None
        """
        widget = QWidget(self)
        layout = QVBoxLayout(widget)
        title = QLabel(instrumentLabel)
        self.lcd = QLCDNumber(self._decimal_places, self)

        # Configure LCD widget
        self.lcd.setSegmentStyle(self.lcd.Flat)
        self.lcd.setSmallDecimalPoint(True)
        self.lcd.setFixedSize(self._instrument_size)
        self.lcd.display(self._value)

        layout.addWidget(self.lcd)
        layout.addWidget(title)

    @Slot(float)
    def on_modified_data(self, value: float):
        self.lcd.display(value)
