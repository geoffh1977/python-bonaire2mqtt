import asyncio
import sys
import os

from logger import _LOGGER
from classes.bonairepyclimate import BonairePyClimate
from classes.mqttclient import mqttClient
from constants import (
    HVAC_MODE_OFF, HVAC_MODE_ON, HVAC_MODE_HEAT, HVAC_MODE_COOL, HVAC_MODE_FAN_ONLY, MAX_TEMP, MIN_TEMP, HEAT_FAN_MODES, 
    COOL_FAN_MODES, NETWORK_CARD, MQTT_HOST, MQTT_KEEP_ALIVE, MQTT_PORT, MQTT_TOPIC_PREFIX)

# Callback For Data From Climate Control To Mqtt
def bonaire_callback():
    # Publish States To MQTT
    _LOGGER.debug('Received Data From Bonaire Wifi Unit.')
    for key in climate._states:
        topic = MQTT_TOPIC_PREFIX + '/' + key + '/get'
        message = climate._states[key]
        mqttc.publish_message(topic = topic, message = message)
    return True

# Callback For Data To Set Climate Control
def mqtt_callback(msg):
    climateKey = msg.topic.split('/')[1]
    value = msg.payload.decode()

    if climateKey == 'system':
        if value in [HVAC_MODE_ON, HVAC_MODE_OFF]:
            climate.set_general(climateKey, value)
            _LOGGER.debug('Received command from MQTT. key: ' + climateKey + ' - value: ' + value)
            return True
        else:
            _LOGGER.error('Invalid ' + climateKey + ' Value received from MQTT.')
            return False

    if climateKey == 'type':
        if value in [HVAC_MODE_HEAT, HVAC_MODE_COOL]:
            climate.set_general('system', 'on')
            climate.set_general(climateKey, value)
            _LOGGER.debug('Received command from MQTT. key: ' + climateKey + ' - value: ' + value)
            return True
        else:
            _LOGGER.error('Invalid ' + climateKey + ' Value received from MQTT.')
            return False

    if climateKey == 'setPoint':
        if int(value) >= MIN_TEMP and int(value) <= MAX_TEMP:
            climate.set_general(climateKey, value)
            _LOGGER.debug('Received command from MQTT. key: ' + climateKey + ' - value: ' + value)
            return True
        else:
            _LOGGER.error('Invalid ' + climateKey + ' Value received from MQTT.')
            return False

    if climateKey == 'mode':
        if climate.get_type() == 'heat':
            if value in HEAT_FAN_MODES:
                climate.set_general('system', 'on')
                climate.set_general(climateKey, value)
                _LOGGER.debug('Received command from MQTT. key: ' + climateKey + ' - value: ' + value)
                return True
            else:
                _LOGGER.error('Invalid ' + climateKey + ' Value received from MQTT.')
                return False
        elif climate.get_type() == 'cool':
            if value in COOL_FAN_MODES:
                climate.set_general('system', 'on')
                climate.set_general(climateKey, value)
                _LOGGER.debug('Received command from MQTT. key: ' + climateKey + ' - value: ' + value)
                return True  
            else:
                _LOGGER.error('Invalid ' + climateKey + ' Value received from MQTT.')
                return False      
        else:
            _LOGGER.error('Invalid ' + climateKey + ' Value received from MQTT.')
            return False

    if climateKey == 'fanSpeed':
        if int(value) >= 1 and int(value) <= 8:
            climate.set_general('system', 'on')
            climate.set_general('mode', HVAC_MODE_FAN_ONLY)
            climate.set_general('type', 'cool')
            _LOGGER.debug('Setting Fan Mode.')
            climate.set_general(climateKey, value)
            _LOGGER.debug('Received command from MQTT. key: ' + climateKey + ' - value: ' + value)
            return True
        else:
            _LOGGER.error('Invalid ' + climateKey + ' Value received from MQTT.')
            return False

    if climateKey == 'zoneList':
        climate.set_general(climateKey, value)
        _LOGGER.debug('Received command from MQTT. key: ' + climateKey + ' - value: ' + value)
        return True
    else:
        _LOGGER.error('Invalid ' + climateKey + ' Value received from MQTT.')
        return False

### Main Function
# Display Name Of Application In Logger
_LOGGER.info('Bonaire2Mqtt is now attempting to start up...')
# Get Local Ip Address
try:
    local_ip = os.popen('ip addr show ' + NETWORK_CARD +' 2> /dev/null').read().split("inet ")[1].split("/")[0]
except IndexError:
    _LOGGER.error('An Invalid Network Card Is Selected.')
    sys.exit(1)

# Create Event Loop
event_loop = asyncio.get_event_loop()

# Register Bonaire Class Details
_LOGGER.info('Initialising Connection To Bonaire Wifi Unit...')
climate = BonairePyClimate(event_loop, local_ip)
climate.register_update_callback(bonaire_callback)

# Register MqttClient Class Details
_LOGGER.info('Initialising Connection To MQTT Broker...')
mqttc = mqttClient(event_loop, mqtt_host=MQTT_HOST, mqtt_port=MQTT_PORT, mqtt_prefix=MQTT_TOPIC_PREFIX, mqtt_keep_alive=MQTT_KEEP_ALIVE)
mqttc.register_update_callback(mqtt_callback)

# Run Loop Forever Or Finish On Interrupt
_LOGGER.info('Starting Event Run Loop...')
try:
    event_loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    _LOGGER.info("Closing Down Application - Disconnecting MQTT Broker")
    mqttc.disconnect()
    event_loop.run_until_complete(event_loop.shutdown_asyncgens())
    event_loop.close()
    _LOGGER.info("Bonaire2Mqtt Shut Down Successfully.")
