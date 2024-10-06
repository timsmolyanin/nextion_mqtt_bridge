import yaml
import json
import logging

logger = logging.getLogger(__name__)

class ConfigLoader:
    def __init__(self, path):
        self.path = path

    def load_config(self):
        try:
            with open(self.path, 'r') as file:
                config = yaml.safe_load(file)
                self.load_additional_configs(config)
                return config
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return None

    def load_additional_configs(self, config):
        if 'mqtt' in config and 'topics_file' in config['mqtt']:
            try:
                with open(config['mqtt']['topics_file'], 'r') as file:
                    config['mqtt']['topics'] = yaml.safe_load(file)
            except Exception as e:
                logger.error(f"Error loading MQTT topics: {e}")
        if 'topic_executor' in config and 'config_file' in config['topic_executor']:
            try:
                with open(config['topic_executor']['config_file'], 'r') as file:
                    config['topic_executor'] = json.load(file)
            except Exception as e:
                logger.error(f"Error loading TopicExecutor configuration: {e}")