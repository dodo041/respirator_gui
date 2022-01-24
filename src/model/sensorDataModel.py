from typing import Deque
from collections import deque
from PySide6.QtCore import QObject, Signal

MAX_QUEUE_LENGTH = 1000


# TODO somehow use this class to abstract signals from actual model
class SensorModelSignals(QObject):
    """
    SensorModelSignals shall be used to inform controller/view about changes in the sensor data models.
    """

    modified_air_pressure_data = Signal
    modified_air_temp_data = Signal
    modified_animal_temp_data = Signal
    modified_heatbed_temp_data = Signal
    modified_eTVOC_data = Signal
    modified_eCO2_data = Signal

    def __init__(self):
        super(SensorModelSignals, self).__init__()

        self.modified_air_pressure_data = Signal(float)
        self.modified_air_temp_data = Signal(float)
        self.modified_animal_temp_data = Signal(float)
        self.modified_heatbed_temp_data = Signal(float)
        self.modified_eTVOC_data = Signal(float)
        self.modified_eCO2_data = Signal(float)


class SensorDataModel(QObject):
    """
    Model for sensor related data.
    """

    # Signals
    modified_air_pressure_data = Signal(float)
    modified_air_temp_data = Signal(float)
    modified_animal_temp_data = Signal(float)
    modified_heatbed_temp_data = Signal(float)
    modified_eTVOC_data = Signal(float)
    modified_eCO2_data = Signal(float)
    modified_relative_humidity_data = Signal(float)

    # Data queues
    _air_pressure_data = Deque
    _air_temp_data = Deque
    _animal_temp_data = Deque
    _heatbed_temp_data = Deque
    _eCO2_data = Deque
    _eTVOC_data = Deque
    _relative_humidity_data = Deque

    _min_pressure_border = float
    _max_pressure_border = float

    def __init__(self):
        """
        The sensor data model consists of independent queues (of type collection.deque). That way reading one sensor
        value from the queue does not depend on another value, which was recorded at the same time instance.
        """
        super(SensorDataModel, self).__init__()

        # Queues (dequeues) with sensor data
        self._air_pressure_data = deque()
        self._air_temp_data = deque()
        self._animal_temp_data = deque()
        self._heatbed_temp_data = deque()
        self._eCO2_data = deque()
        self._eTVOC_data = deque()
        self._relative_humidity_data = deque()

        # Borders for pressure alarm
        self._min_pressure_border = float()
        self._max_pressure_border = float()

    # Global getters and setters

    @property
    def air_pressure_data(self) -> deque:
        return self._air_pressure_data

    @air_pressure_data.setter
    def air_pressure_data(self, data: float):
        self._cut_long_queue(self._air_pressure_data, MAX_QUEUE_LENGTH)
        self._air_pressure_data.append(data)
        self.modified_air_pressure_data.emit(data)

    @property
    def air_temp_data(self) -> deque:
        return self._air_temp_data

    @air_temp_data.setter
    def air_temp_data(self, data: float):
        self._cut_long_queue(self._air_temp_data, MAX_QUEUE_LENGTH)
        self._air_temp_data.append(data)
        self.modified_air_temp_data.emit(data)

    @property
    def animal_temp_data(self) -> deque:
        return self._animal_temp_data

    @animal_temp_data.setter
    def animal_temp_data(self, data: float):
        self._cut_long_queue(self._animal_temp_data, MAX_QUEUE_LENGTH)
        self._animal_temp_data.append(data)
        self.modified_animal_temp_data.emit(data)

    @property
    def heatbed_temp_data(self) -> deque:
        return self._heatbed_temp_data

    @heatbed_temp_data.setter
    def heatbed_temp_data(self, data: float):
        self._cut_long_queue(self._heatbed_temp_data, MAX_QUEUE_LENGTH)
        self._heatbed_temp_data.append(data)
        self.modified_heatbed_temp_data.emit(data)

    @property
    def eCO2_data(self) -> deque:
        return self._eCO2_data

    @eCO2_data.setter
    def eCO2_data(self, data: float):
        self._cut_long_queue(self._eCO2_data, MAX_QUEUE_LENGTH)
        self._eCO2_data.append(data)
        self.modified_eCO2_data.emit(data)

    @property
    def eTVOC_data(self) -> deque:
        return self._eTVOC_data

    @eTVOC_data.setter
    def eTVOC_data(self, data: float):
        self._cut_long_queue(self._eTVOC_data, MAX_QUEUE_LENGTH)
        self._eTVOC_data.append(data)
        self.modified_eTVOC_data.emit(data)

    @property
    def relative_humidity_data(self) -> deque:
        return self._relative_humidity_data

    @relative_humidity_data.setter
    def relative_humidity_data(self, data: float):
        self._cut_long_queue(self._relative_humidity_data, MAX_QUEUE_LENGTH)
        self._relative_humidity_data.append(data)
        self.modified_relative_humidity_data.emit(data)

    @property
    def min_pressure_border(self) -> float:
        return self._min_pressure_border

    @min_pressure_border.setter
    def min_pressure_border(self, min_pressure: float):
        self._min_pressure_border = min_pressure

    @property
    def max_pressure_border(self) -> float:
        return self._max_pressure_border

    @max_pressure_border.setter
    def max_pressure_border(self, max_pressure: float):
        self._max_pressure_border = max_pressure

    @staticmethod
    def _cut_long_queue(queue: Deque, max_queue_length: int) -> None:
        """
        Shortens a deque type queue in case it exceeds a maximum length (oldest queue entry is being removed).

        :param queue: Deque type queue
        :param max_queue_length: Maximum allowed length of the queue
        :return: None
        """
        if len(queue) > max_queue_length:
            queue.popleft()
