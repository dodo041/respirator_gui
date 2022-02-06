import logging
from serial import Serial
from serial.tools import list_ports
from serial.serialutil import SerialException

# Raspberry Pi Pico vendor + product IDs
# see https://github.com/raspberrypi/usb-pid
PICO_VENDOR_ID = 11914
PICO_BOOT_PRODUCT_ID = 0x0003
PICO_CDC_PRODUCT_ID = 0x000A

# Timeout for reading from / writing to devices [seconds]
TIMEOUT = 0.5
# Maximum buffer size for reading [bytes]
READ_BUFFER_SIZE = 128


def _find_pico_com_port() -> str | None:
    """
    Find Raspberry Pi Pico (as "Raspberry Pi Pico SDK CDC UART") and the COM port at which it's connected to
    :return: COM port at which the Raspberry Pi Pico is connected to; None if not found
    """
    # TODO maybe add retry mechanism, user should also be able to trigger it himself if necessary
    # TODO (e.g. when connection is lost after it was established before)
    logging.info("Scanning serial ports on device")
    for port in list_ports.comports():
        if port.vid == PICO_VENDOR_ID and port.pid == PICO_CDC_PRODUCT_ID:
            logging.info(f"Found Raspberry Pi Pico at {port.name}")
            return port.name
        else:
            logging.warning("Could not find Raspberry Pi Pico connected to your device. Please check the connection "
                            "and try again.")
            return None


class PicoUSBController:
    """
    PicoUSBController manages the connection and communication from and to the Raspberry Pi Pico.
    """

    _serial_controller = Serial
    _PICO_COM_PORT = ""

    def __init__(self):
        logging.debug("Creating new USB controller for Raspberry Pi Pico")
        self._PICO_COM_PORT = _find_pico_com_port()

        if self._PICO_COM_PORT is not None and not "":
            # Initialize CDC connection to Raspberry Pi Pico
            self._serial_controller = Serial(port=self._PICO_COM_PORT, timeout=TIMEOUT)
            logging.debug(f"Successfully initialised serial port {self._PICO_COM_PORT}")
        else:
            raise SerialException("Could not find Raspberry Pi Pico connected to your device. Please check the "
                                  "connection and try again.")

    def read_from_pico(self) -> bytes:
        data = self._serial_controller.readline(READ_BUFFER_SIZE)
        logging.debug(f"Read data from Raspberry Pi Pico: {data}")
        return data

    def write_to_pico(self, data: bytes) -> bool:
        logging.debug(f"Sending data to Raspberry Pi Pico: {data}")
        try:
            self._serial_controller.write(data)
        except SerialException:
            logging.error(f"Could not send data to Raspberry Pi Pico: {data}")
            return False
        else:
            logging.info("Successfully sent preset to Raspberry Pi Pico")
            return True
