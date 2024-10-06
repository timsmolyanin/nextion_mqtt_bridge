import time
from serial_interface import SerialInterface
from mqtt_interface import MQTTInterface
from topic_executor import TopicExecutor
import logging

logger = logging.getLogger(__name__)

class NextionMqttBridge:
    def __init__(self, config):
        self.config = config
        self.serial = SerialInterface(self.config['serial'])
        self.mqtt = MQTTInterface(self.config['mqtt'])
        self.topic_executor = TopicExecutor(self.serial, self.config['topic_executor'])

    def start(self):
        self.mqtt.set_on_message_callback(self.on_mqtt_message)
        self.mqtt.connect()
        self.mqtt.subscribe_to_topics()
        self.mqtt.loop_start()  # Start the MQTT client in a background thread
        self.serial.connect()

        self.read_from_serial()

    def read_from_serial(self):
        while True:
            data = self.serial.read_line()
            if data:
                self.handle_serial_data(data)
            time.sleep(0.1)

    def handle_serial_data(self, data):
        try:
            array_data = data.split(":")
            if len(array_data) != 3:
                logger.error(f"Invalid data format from serial port: {data}")
                return

            widget_name, topic, value = array_data

            self.mqtt.publish(topic, value)
            logger.debug(f"Published to MQTT topic {topic}: {value}")
        except ValueError:
            logger.error(f"Invalid data format from serial port: {data} widget name {widget_name}")

    def on_mqtt_message(self, topic, payload):
        self.topic_executor.execute(topic, payload)