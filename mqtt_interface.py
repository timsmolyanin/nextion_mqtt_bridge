import paho.mqtt.client as mqtt
import logging

logger = logging.getLogger(__name__)

class MQTTInterface:
    def __init__(self, config):
        self.client = mqtt.Client()
        self.broker = config['broker']
        self.port = config['port']
        self.topics = config['topics']
        self.username = config.get('username')
        self.password = config.get('password')
        if self.username and self.password:
            self.client.username_pw_set(self.username, self.password)
        self.on_message_callback = None

    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self._on_message
        self.client.connect(self.broker, self.port)
        logger.info(f"Connecting to MQTT broker {self.broker}:{self.port}")

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            logger.info("Successfully connected to MQTT")
        else:
            logger.error(f"Failed to connect to MQTT with code {rc}")

    def subscribe_to_topics(self):
        for topic in self.topics:
            self.client.subscribe(topic['topic'], qos=topic.get('qos', 0))
            logger.info(f"Subscribed to topic: {topic['topic']}")

    def set_on_message_callback(self, callback):
        self.on_message_callback = callback

    def _on_message(self, client, userdata, msg):
        payload = msg.payload.decode('utf-8')
        if self.on_message_callback:
            self.on_message_callback(msg.topic, payload)

    def publish(self, topic, payload):
        self.client.publish(topic, payload)
        logger.debug(f"Published {payload} to topic {topic}")

    def loop_start(self):
        self.client.loop_start()