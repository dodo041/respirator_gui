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

    # Signals
    modified_air_pressure_data = Signal(float)
    modified_air_temp_data = Signal(float)
    modified_animal_temp_data = Signal(float)
    modified_heatbed_temp_data = Signal(float)
    modified_eTVOC_data = Signal(float)
    modified_eCO2_data = Signal(float)
    modified_relative_humidity_data = Signal(float)

    # Data queues
    air_pressure_data = Deque
    air_temp_data = Deque
    animal_temp_data = Deque
    heatbed_temp_data = Deque
    eCO2_data = Deque
    eTVOC_data = Deque
    relative_humidity_data = Deque

    min_pressure_border = float
    max_pressure_border = float

    def __init__(self):
        """
        The sensor data model consists of independent queues (of type collection.deque). That way reading one sensor
        value from the queue does not depend on another value, which was recorded at the same time instance.
        """
        super(SensorDataModel, self).__init__()

        # Queues (dequeues) with sensor data
        self.air_pressure_data = deque()
        self.air_temp_data = deque()
        self.animal_temp_data = deque()
        self.heatbed_temp_data = deque()
        self.eCO2_data = deque()
        self.eTVOC_data = deque()
        self.relative_humidity_data = deque()

        # Borders for pressure alarm
        self.min_pressure_border = float()
        self.max_pressure_border = float()

    # Methods for writing data to specific sensor model
    # TODO maybe there's a more elegant way of doing this to avoid code duplication? e.g. binding signals to model?

    def write_air_pressure_data(self, data: float):
        self._cut_long_queue(self.air_pressure_data, MAX_QUEUE_LENGTH)
        self.air_pressure_data.append(data)
        self.modified_air_pressure_data.emit(data)

    def write_air_temp_data(self, data: float):
        self._cut_long_queue(self.air_temp_data, MAX_QUEUE_LENGTH)
        self.air_temp_data.append(data)
        self.modified_air_temp_data.emit(data)

    def write_animal_temp_data(self, data: float):
        self._cut_long_queue(self.animal_temp_data, MAX_QUEUE_LENGTH)
        self.animal_temp_data.append(data)
        self.modified_animal_temp_data.emit(data)

    def write_heatbed_temp_data(self, data: float):
        self._cut_long_queue(self.heatbed_temp_data, MAX_QUEUE_LENGTH)
        self.heatbed_temp_data.append(data)
        self.modified_heatbed_temp_data.emit(data)

    def write_eTVOC_data(self, data: float):
        self._cut_long_queue(self.eTVOC_data, MAX_QUEUE_LENGTH)
        self.eTVOC_data.append(data)
        self.modified_eTVOC_data.emit(data)

    def write_eCO2_data(self, data: float):
        self._cut_long_queue(self.eCO2_data, MAX_QUEUE_LENGTH)
        self.eCO2_data.append(data)
        self.modified_eCO2_data.emit(data)

    def write_relative_humidity_data(self, data: float):
        self._cut_long_queue(self.relative_humidity_data, MAX_QUEUE_LENGTH)
        self.relative_humidity_data.append(data)
        self.modified_relative_humidity_data.emit(data)

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
