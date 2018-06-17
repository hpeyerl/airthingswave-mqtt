import yaml
import logging
import paho.mqtt.client as mqtt
from bluepy.btle import UUID, Peripheral
from datetime import datetime
import sys
import time
import struct
import re

class Sensor:
    def __init__(self, name, uuid, format_type, unit, scale):
        self.name = name
        self.uuid = uuid
        self.format_type = format_type
        self.unit = unit
        self.scale = scale

class AirthingsWave_mqtt:
    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            self.config=yaml.load(f)
        self.waves=list()
        if self.check_config(self.config):
            self.mqtt_client = mqtt.Client()
        self.sensors = []
        self.sensors.append(Sensor("DateTime", UUID(0x2A08), 'HBBBBB', "\t", 0))
        self.sensors.append(Sensor("Temperature", UUID(0x2A6E), 'h', "deg C\t", 1.0/100.0))
        self.sensors.append(Sensor("Humidity", UUID(0x2A6F), 'H', "%\t\t", 1.0/100.0))
        self.sensors.append(Sensor("Radon 24h avg", "b42e01aa-ade7-11e4-89d3-123b93f75cba", 'H', "Bq/m3\t", 1.0))
        self.sensors.append(Sensor("Radon long term", "b42e0a4c-ade7-11e4-89d3-123b93f75cba", 'H', "Bq/m3\t", 1.0))

    def check_config(self, conf):
        if "mqtt" not in conf:
            return false
        if "broker" not in conf["mqtt"]:
            return false
        if "port" not in conf["mqtt"]:
            return false
        if "waves" in conf:
            for wave in conf["waves"]:
                if "addr" in wave and "name" in wave:
                    self.waves.append(wave)
                else:
                    print("Malformed config item: {0}".format(wave))

    def mqtt_connect(self, conf):
	self.mqtt_conf=self.config["mqtt"]
	self.mqtt_client.connect(conf["broker"], conf["port"])

    def ble_connect(self, addr):
	p = Peripheral(addr)
	return p

    def ble_disconnect(self, p)
       p.disconnect()

    def get_readings(self, p, addr):
        str_out = ""
        for s in self.sensors:
            ch  = p.getCharacteristics(uuid=s.uuid)[0]
            if (ch.supportsRead()):
                val = ch.read()
                val = struct.unpack(s.format_type, val)
                if s.name == "DateTime":
                    str_out += str(datetime(val[0], val[1], val[2], val[3], val[4], val[5])) + s.unit
                else:
                    str_out += str(val[0] * s.scale) + " " + s.unit
		readings[s.name]=str_out
	
        return readings
