import argparse
import logging
from nextion_mqtt_bridge import NextionMqttBridge
from config_loader import ConfigLoader


def parse_arguments():
    parser = argparse.ArgumentParser(description='Nextion MQTT Bridge')
    parser.add_argument('-c', '--config', default='config/app_config.yaml', help='Path to the configuration file')
    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    config_loader = ConfigLoader(args.config)
    config = config_loader.load_config()

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    bridge = NextionMqttBridge(config)
    bridge.start()

if __name__ == '__main__':
    main()
