import os

# Bonaire MyClimate Constants
DELETE = "<myclimate><delete>connection</delete></myclimate>"
DISCOVERY = "<myclimate><get>discovery</get><ip>{}</ip><platform>android</platform><version>1.0.0</version></myclimate>"
EVAP_FAN_MODES = ['thermo']
EVAP_MAX_TEMP = 8
EVAP_MIN_TEMP = 1
FAN_ONLY_FAN_MODES = ['1', '2', '3', '4', '5', '6', '7', '8']
GETZONEINFO = "<myclimate><get>getzoneinfo</get><zoneList>1,2</zoneList></myclimate>"
INSTALLATION = "<myclimate><get>installation</get></myclimate>"
LOCAL_PORT = 10003
POSTZONEINFO = "<myclimate><post>postzoneinfo</post><system>{system}</system><type>{type}</type><zoneList>{zoneList}</zoneList><mode>{mode}</mode><setPoint>{setPoint}</setPoint></myclimate>"
POSTZONEINFOFAN = "<myclimate><post>postzoneinfo</post><system>{system}</system><type>{type}</type><zoneList>{zoneList}</zoneList><mode>{mode}</mode><fanSpeed>{fanSpeed}</fanSpeed></myclimate>"
UDP_DISCOVERY_PORT = 10001
MAX_TEMP = 32
MIN_TEMP = 10
HEAT_FAN_MODES = ['econ', 'thermo', 'boost']
COOL_FAN_MODES = ['thermo']

# MQTT Contstants
MQTT_HOST = os.getenv('MQTT_HOST', '127.0.0.1')
MQTT_PORT = os.getenv('MQTT_PORT', '1883')
MQTT_KEEP_ALIVE = os.getenv('MQTT_KEEP_ALIVE', '60')
MQTT_TOPIC_PREFIX = os.getenv('MQTT_PREFIX', 'bonaire')

# Shared Constants
CLIMATE_KEYS = ['system', 'type', 'zoneList', 'mode', 'setPoint', 'roomTemp', 'fanSpeed']
HVAC_MODE_OFF = 'off'
HVAC_MODE_ON = 'on'
HVAC_MODE_HEAT = 'heat'
HVAC_MODE_COOL = 'cool'
HVAC_MODE_FAN_ONLY = 'fan'

NETWORK_CARD = os.getenv('NETWORK_CARD', 'eth0')