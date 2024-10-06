import serial
import time
import logging

logger = logging.getLogger(__name__)

class SerialInterface:
    def __init__(self, config):
        self.port = config['port']
        self.baudrate = config['baudrate']
        self.timeout = config.get('timeout', 1)
        self.open_retry_interval = config.get('open_retry_interval', 5)
        self.serial = None

    def connect(self):
        while True:
            try:
                self.serial = serial.Serial(
                    port=self.port,
                    baudrate=self.baudrate,
                    timeout=self.timeout
                )
                logger.info(f"Connected to serial port {self.port}")
                break
            except serial.SerialException as e:
                logger.error(f"Error connecting to serial port: {e}")
                time.sleep(self.open_retry_interval)

    def read_line(self):
        try:
            line = self.serial.readline().decode('utf-8').strip()
            if line:
                logger.debug(f"Received from serial port: {line}")
            return line
        except Exception as e:
            logger.error(f"Error reading from serial port: {e}")
            return None

    def write(self, data):
        try:
            eof = bytes([0xFF, 0xFF, 0xFF])
            self.serial.write(data.encode('utf-8') + eof)
            logger.debug(f"Sent to serial port: {data}")
        except Exception as e:
            logger.error(f"Error writing to serial port: {e}")