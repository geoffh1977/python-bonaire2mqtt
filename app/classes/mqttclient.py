import asyncio
import sys
import os
import socket
import aiomqtt
import time

from logger import _LOGGER
from constants import CLIMATE_KEYS

class mqttClient():
    def __init__(self, event_loop, mqtt_host='127.0.0.1', mqtt_port=1883, mqtt_keep_alive=60, mqtt_prefix='test'):
        self._event_loop = event_loop
        self._update_callback = None
        self._mqtt_host = mqtt_host
        self._mqtt_port = int(mqtt_port)
        self._mqtt_keep_alive = int(mqtt_keep_alive)
        self._mqtt_prefix = mqtt_prefix

        self._event_loop.create_task(self.start())

    def on_connect(self, client, userdata, flags, rc):
        self.connected.set()
    
    def on_message(self, mosq, obj, msg):
        _LOGGER.debug('Received From MQTT! Topic: '+ msg.topic +' = '+ msg.payload.decode())
        if self._update_callback is not None:
            self._update_callback(msg)

    def on_subscribe(self, client, userdata, mid, granted_qos):
        self.subscribed.set()

    def on_disconnect(self, client, userdata, rc):
        self.disconnected.set()

    async def start(self):
        self.connected = asyncio.Event()
        self.subscribed = asyncio.Event()
        self.disconnected = asyncio.Event()

        self.mqttc = aiomqtt.Client(self._event_loop)

        self.mqttc.loop_start()

        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.on_message = self.on_message
        self.mqttc.on_disconnect = self.on_disconnect

        await self.mqttc.connect(self._mqtt_host, self._mqtt_port, self._mqtt_keep_alive)
        await self.connected.wait()
        _LOGGER.info('Succssfully Connect To MQTT Broker On ' + self._mqtt_host + ':' + str(self._mqtt_port))

        for climate_key in CLIMATE_KEYS:
            self.subscribe_topic(self._mqtt_prefix + '/' + climate_key + '/set')

        # Main Wait Point
        await self.disconnected.wait()
    
        _LOGGER.info('Disconnected From MQTT Successfully')
        await self.mqttc.loop_stop()
        _LOGGER.info('MQTT Class Has Completed!')

    def subscribe_topic(self, topic = None, qos = 0):
        if topic is None:
            return False
        self.mqttc.subscribe(topic = topic, qos = qos)
        _LOGGER.debug('Subscribed To Topic: ' + topic)

    def publish_message(self, topic=None, message=None):
        if topic is None:
            return False
        if message is None:
            return False
        self.mqttc.publish(topic, message)
        _LOGGER.debug('Publish Successful. Topic: ' + topic + ' = ' + message)

    def register_update_callback(self, method):
        self._update_callback = method


    def disconnect(self):
        asyncio.sleep(1)
        _LOGGER.info('Disconnecting From MQTT...')
        self.mqttc.disconnect()
