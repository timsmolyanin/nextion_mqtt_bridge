import json
import ast

# Функция для чтения JSON файла
def read_json_file(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Функция для чтения Python файла и извлечения списка MQTT топиков
def extract_mqtt_topics(py_path):
    with open(py_path, 'r', encoding='utf-8') as file:
        py_content = file.read()
        # Преобразуем содержимое в абстрактное синтаксическое дерево (AST)
        parsed = ast.parse(py_content)
        # Проходимся по узлам дерева, ищем нужный список
        for node in ast.walk(parsed):
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
                if node.targets[0].id == 'list_of_mqtt_topics':
                    return [topic[0] for topic in ast.literal_eval(node.value)]
    return []

# Функция для создания путей из JSON структуры
def generate_paths_from_json(data):
    paths = []
    for main_key, sub_dict in data.items():
        for sub_key in sub_dict.keys():
            path = f"/devices/{main_key}/controls/{sub_key}"
            paths.append(path)
    return paths

# Основная функция
def main(json_file, py_file):
    json_data = read_json_file(json_file)
    python_mqtt_topics = extract_mqtt_topics(py_file)
    
    json_paths = generate_paths_from_json(json_data)
    
    # Проверяем, есть ли пути из JSON в списке MQTT топиков из .py файла
    for path in json_paths:
        if path not in python_mqtt_topics:
            print(f"Path {path} is missing.")

# Пример вызова функции
json_file_path = 'NextionMqttBridgeConfig.json'
py_file_path = 'list_of_mqtt_topics.py'

main(json_file_path, py_file_path)
print('Done')
