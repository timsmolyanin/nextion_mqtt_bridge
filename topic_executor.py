class TopicExecutor:
    
    def __init__(self,nextion_mqtt_bridge, config):
        self.nextion_mqtt_bridge = nextion_mqtt_bridge
        
        self.config = config
    
    def execute(self, group_name, module_name, topic_value):
        try:
            module = self.config[group_name][module_name]
        except KeyError:
            raise KeyError('Ключ не найден, топик не прописан', group_name, module_name)
        
        if module['Condition'] == 'Default':
            try:
                cmds = module["Cmd"]
                if module["Type"] == 'txt':
                    for cmd in cmds:
                        full_cmd = f'{cmd}\"{topic_value}\"'
                        self.nextion_mqtt_bridge.serial_write(full_cmd)
                
                if module["Type"] == 'val':
                    for cmd in cmds:
                        full_cmd = f'{cmd}{topic_value}'
                        self.nextion_mqtt_bridge.serial_write(full_cmd)

            except Exception as e:
                print(e)
          

        if module['Condition'] == 'State':
            try:
                cmds = module[str(topic_value)]
            except KeyError:
                raise KeyError('Состояния "' + str(topic_value) + '" в модуле "' + module_name + '" не существует. Группа: "' + group_name + '"')
            for cmd in cmds:
                self.nextion_mqtt_bridge.serial_write(cmd)


        if module['Condition'] == 'NonStrict Range':
            for range in module['Ranges']:
                if module[range]['From'] <= topic_value <= module[range]['To']:
                    try:
                        cmds = module[range]["Cmd"]
                        for cmd in cmds:
                            self.nextion_mqtt_bridge.serial_write(cmd)
                    except Exception as e:
                        print(e)
                
        if module['Condition'] == 'Strict Range':
            for range in module['Ranges']:
                if module[range]['From'] < topic_value < module[range]['To']:
                    try:
                        cmds = module[range]["Cmd"]
                        for cmd in cmds:
                            self.nextion_mqtt_bridge.serial_write(cmd)
                    except Exception as e:
                        print(e)

        