# Nextion MQTT Bridge
## Описание проекта

Nextion MQTT Bridge — это приложение на Python, предназначенное для организации мостика между дисплеем Nextion и брокером MQTT. Оно обеспечивает двустороннюю связь: получает данные с дисплея Nextion и публикует их в MQTT-топики, а также подписывается на MQTT-топики и отправляет соответствующие команды на дисплей Nextion.

### Структура проекта

Проект состоит из следующих файлов и директорий:

    main.py: основной файл для запуска приложения.
    nextion_mqtt_bridge.py: класс, реализующий логику моста между Nextion и MQTT.
    serial_interface.py: модуль для работы с последовательным портом.
    mqtt_interface.py: модуль для работы с MQTT.
    topic_executor.py: модуль для обработки топиков и выполнения соответствующих команд.
    config_loader.py: модуль для загрузки конфигурационных файлов.
    config/: директория для хранения конфигурационных файлов:
        app_config.yaml: основной файл конфигурации приложения.
        mqtt_topics.yaml: список MQTT-топиков для подписки.
        topic_config.json: конфигурация для TopicExecutor.
    requirements.txt: файл с зависимостями проекта.

## Установка и запуск
Чуть позже появится еще инфо.

### Настройка конфигурационных файлов

В директории config находятся три файла конфигурации:

    app_config.yaml: основной файл конфигурации приложения.
    mqtt_topics.yaml: список MQTT-топиков для подписки.
    topic_config.json: конфигурация для TopicExecutor.

Пример app_config.yaml

```yaml

serial:
  port: "/dev/ttyS4"
  baudrate: 115200
  timeout: 1
  open_retry_interval: 5

mqtt:
  broker: "192.168.44.10"
  port: 1883
  username: null
  password: null
  topics_file: "config/mqtt_topics.yaml"

topic_executor:
  config_file: "config/topic_config.json"
```
Настройте следующие параметры:

***serial.port***: укажите порт последовательного интерфейса (например, /dev/ttyS4 для Linux или COM3 для Windows).

serial.baudrate: скорость передачи данных (обычно 115200).

mqtt.broker: адрес вашего MQTT-брокера.

mqtt.port: порт MQTT-брокера (обычно 1883).

mqtt.username и mqtt.password: при необходимости укажите учетные данные для аутентификации на MQTT-брокере.

Пример mqtt_topics.yaml

Содержит список топиков MQTT, на которые приложение будет подписываться:

```yaml

- topic: "/devices/wb-mrwm2_129/controls/K1"
  qos: 0
- topic: "//devices/wb-mrwm2_129/controls/K2"
  qos: 0
# Добавьте остальные топики здесь
```
Настройте список топиков в соответствии с вашими потребностями.
Пример topic_config.json

Содержит конфигурацию для TopicExecutor, определяющую, какие команды должны выполняться при получении определенных сообщений по MQTT.

```json

{
  "wb-mrwm2_129": {
    "K1": {
      "Condition": "State",
      "0": ["electricity.BTN_ROOM1.picc=19"],
      "1": ["electricity.BTN_ROOM1.picc=20"]
    },
    "K2": {
      "Condition": "State",
      "0": ["electricity.BTN_ROOM2.picc=19"],
      "1": ["electricity.BTN_ROOM2.picc=20"]
    }
  }
}
```
Настройте конфигурацию в соответствии с вашими устройствами и командами.

### Запуск приложения

Запустите приложение командой:

```bash
python main.py -c config/app_config.yaml
```
Параметр `-c` указывает путь к файлу конфигурации. Если его опустить, по умолчанию используется `config/app_config.yaml`.

### Примеры использования
#### Пример 1
Сценарий:

    У вас есть устройство wb-mrwm2_129 с контролами K1 и K2.
    Когда приходит сообщение по топику /devices/wb-mrwm2_129/controls/K1 со значением 1, вы хотите изменить картинку на дисплее Nextion.

Настройка topic_config.json:

```json

{
  "wb-mrwm2_129": {
    "K1": {
      "Condition": "State",
      "0": ["electricity.BTN_ROOM1.picc=19"],
      "1": ["electricity.BTN_ROOM1.picc=20"]
    }
  }
}
```
Объяснение:

    При получении значения 0 по топику /devices/wb-mrwm2_129/controls/K1 будет отправлена команда electricity.BTN_ROOM1.picc=19 на дисплей Nextion.
    При получении значения 1 будет отправлена команда electricity.BTN_ROOM1.picc=20.

Дополнительные настройки

    Логирование: уровень логирования можно настроить в файле main.py. По умолчанию установлен уровень INFO. Для более подробного логирования измените его на DEBUG:

```python
logging.basicConfig(level=logging.DEBUG)
```
Аутентификация MQTT: если ваш MQTT-брокер требует аутентификации, укажите имя пользователя и пароль в файле app_config.yaml:
```yaml
mqtt:
  broker: "192.168.44.10"
  port: 1883
  username: "your_username"
  password: "your_password"
  topics_file: "config/mqtt_topics.yaml"
```
Настройка времени ожидания и повторныхподключений: в файле app_config.yaml можнонастроить параметры timeout иopen_retry_interval для последовательногопорта.

#### Пример 2
Сценарий:
Отображение температуры на дисплее

Цель: Получать данные температуры с датчика и отображать их на дисплее Nextion.

Настройка mqtt_topics.yaml:

```yaml
- topic: "/devices/temperature/controls/current"
  qos: 0
```
Настройка topic_config.json:

```json
{
  "temperature": {
    "current": {
      "Condition": "Default",
      "Type": "txt",
      "Cmd": ["main.temp_display.txt="]
    }
  }
}
```
Объяснение:

    При получении значения по топику /devices/temperature/controls/current, TopicExecutor выполнит команду main.temp_display.txt="value" на дисплее Nextion, где value — полученное значение температуры.

#### Пример 3
Сценарий:
Управление состоянием кнопки

Цель: Изменять изображение кнопки на дисплее в зависимости от состояния устройства.

Настройка mqtt_topics.yaml:

```yaml
- topic: "/devices/device123/controls/status"
  qos: 0
```
Настройка topic_config.json:

```json
{
  "device123": {
    "status": {
      "Condition": "State",
      "ON": ["main.button.pic=1"],
      "OFF": ["main.button.pic=2"]
    }
  }
}
```
Объяснение:

    Если по топику /devices/device123/controls/status приходит значение ON, на дисплей отправляется команда main.button.pic=1.
    Если значение OFF, отправляется команда main.button.pic=2.

Решение возможных проблем
Приложение не подключается к последовательному порту

    Проверьте правильность указания порта в app_config.yaml.
    Убедитесь, что порт не занят другим приложением.
    Проверьте права доступа к последовательному порту (особенно в Linux-системах).

Не удается подключиться к MQTT-брокеру

    Проверьте адрес и порт брокера в app_config.yaml.
    Убедитесь, что брокер работает и доступен.
    Если используется аутентификация, проверьте правильность имени пользователя и пароля.

Команды не отправляются на дисплей Nextion

    Убедитесь, что конфигурация в topic_config.json соответствует получаемым топикам и значениям.
    Проверьте формат данных, отправляемых с дисплея Nextion.
    Проверьте лог-файлы для поиска возможных ошибок.

Заключение

Nextion MQTT Bridge — удобный инструмент для интеграции дисплеев Nextion с системой MQTT. Благодаря гибкой настройке и модульной структуре кода, приложение можно легко адаптировать под различные задачи и расширять его функциональность.

Если у вас возникнут вопросы или предложения по улучшению проекта, пожалуйста, открывайте новые issues или pull requests в репозитории проекта.