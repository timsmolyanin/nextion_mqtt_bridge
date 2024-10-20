import logging
import json

logger = logging.getLogger(__name__)


class TopicExecutor:
    def __init__(self, serial_interface, config):
        self.serial = serial_interface
        self.config = config

    def execute(self, topic, value):
        try:
            module = self.find_module(topic)
            condition = module['Condition']
            if condition == 'Default':
                self.handle_default(module, value)
            elif condition == 'State':
                self.handle_state(module, value)
            elif condition == 'NonStrict Range':
                self.handle_non_strict_range(module, value)
            elif condition == 'Strict Range':
                self.handle_strict_range(module, value)
            elif condition == 'Transform':
                self.handle_transform_payload(module, value)
            else:
                logger.error(f"Unknown condition type: {condition}")
        except Exception as e:
            logger.error(f"Error while processing a topic {topic}: {e}")

    def find_module(self, topic):
        # expected topic format: /devices/{group}/controls/{module}
        topic_parts = topic.strip('/').split('/')
        if len(topic_parts) < 4:
            raise ValueError(f"Incorrect topic fromat: {topic}")
        _, group, _, module = topic_parts[:4]

        group_config = self.config.get(group)
        if not group_config:
            raise KeyError(f"The group '{group}' is not found in configuration")
        module_config = group_config.get(module)
        if not module_config:
            raise KeyError(f"The module '{module}' is not found in configuration '{group}'")
        return module_config

    def handle_default(self, module, value):
        cmds = module['Cmd']
        cmd_type = module['Type']
        for cmd in cmds:
            if cmd_type == 'txt':
                full_cmd = f'{cmd}"{value}"'
            elif cmd_type == 'val':
                full_cmd = f'{cmd}{value}'
            else:
                logger.error(f"Unkown command type: {cmd_type}")
                continue
            self.serial.write(full_cmd)

    def handle_state(self, module, value):
        cmds = module.get(value)
        if cmds:
            for cmd in cmds:
                self.serial.write(cmd)
        else:
            logger.error(f"State '{value}' is not found in module")

    def handle_non_strict_range(self, module, value):
        try:
            value = float(value)
            for range_config in module['Ranges'].values():
                if float(range_config['From']) <= value <= float(range_config['To']):
                    for cmd in range_config['Cmd']:
                        self.serial.write(cmd)
        except ValueError:
            logger.error(f"Invalid value for range comparison: {value}")

    def handle_strict_range(self, module, value):
        try:
            value = float(value)
            for range_config in module['Ranges'].values():
                if float(range_config['From']) < value < float(range_config['To']):
                    for cmd in range_config['Cmd']:
                        self.serial.write(cmd)
        except ValueError:
            logger.error(f"Invalid value for range comparison: {value}")
    
    def handle_transform_payload(self, module, value):
        try:
            payload_dict = json.loads(value)
            for var, value in payload_dict.items():
                for cmd in module.get(var):
                    full_cmd = f'{cmd}"{value}"' 
                    self.serial.write(full_cmd)
        except Exception as e:
            logger.error(f"handle_transform_payload {e}")
        
