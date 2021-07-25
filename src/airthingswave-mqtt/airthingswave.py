#
# Portions of this code from https://airthings.com/raspberry-pi/ which is itself
# released under an MIT license with the following terms:
#
#        Copyright (c) 2018 Airthings AS
#
#        Permission is hereby granted, free of charge, to any person obtaining a copy
#        of this software and associated documentation files (the "Software"), to deal
#        in the Software without restriction, including without limitation the rights
#        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#        copies of the Software, and to permit persons to whom the Software is
#        furnished to do so, subject to the following conditions:
#       
#        The above copyright notice and this permission notice shall be included in all
#        copies or substantial portions of the Software.
#       
#        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#        SOFTWARE.
#       
#        https://airthings.com
#
#
import yaml
import paho.mqtt.client as mqtt
from bluepy.btle import UUID, Peripheral
from datetime import datetime
import time
import struct


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
            self.config = yaml.load(f, Loader=yaml.SafeLoader)
        self.waves = list()
        if self.check_config(self.config):
            self.mqtt_client = mqtt.Client()
            self.mqtt_connect(self.config)
        self.mqtt_conf = []

        # These are only used for the wave version 1 devices. The code for the version 2 devices hard-codes the order
        # of these sensors when it outputs device readings, so update the V2 order in get_readings_v2() if changing
        # the list of sensors here.
        self.sensors = []
        self.sensors.append(Sensor("DateTime", UUID(0x2A08), 'HBBBBB', "\t", 0))
        self.sensors.append(Sensor("Temperature", UUID(0x2A6E), 'h', "deg C\t", 1.0/100.0))
        self.sensors.append(Sensor("Humidity", UUID(0x2A6F), 'H', "%\t\t", 1.0/100.0))
        self.sensors.append(Sensor("Radon-Day", "b42e01aa-ade7-11e4-89d3-123b93f75cba", 'H', "Bq/m3\t", 1.0))
        self.sensors.append(Sensor("Radon-Long-Term", "b42e0a4c-ade7-11e4-89d3-123b93f75cba", 'H', "Bq/m3\t", 1.0))

    def __del__(self):
        self.mqtt_disconnect()

    def check_config(self, conf):
        if "mqtt" not in conf:
            return False
        if "broker" not in conf["mqtt"]:
            return False
        if "port" not in conf["mqtt"]:
            return False
        if "waves" in conf:
            for wave in conf["waves"]:
                if "addr" in wave and "name" in wave:
                    self.waves.append(wave)
                    if "version" not in wave:
                        self.waves[-1]["version"] = 1
                else:
                    print("Malformed config item: {0}".format(wave))
        return True

    def mqtt_connect(self, conf):
        self.mqtt_conf = conf["mqtt"]
        if self.mqtt_conf["username"]:
            self.mqtt_client.username_pw_set(self.mqtt_conf["username"], self.mqtt_conf["password"])
        self.mqtt_client.connect(self.mqtt_conf["broker"], int(self.mqtt_conf["port"]))

    def mqtt_disconnect(self):
        self.mqtt_client.disconnect()

    def ble_connect(self, addr):
        p = Peripheral(addr)
        return p

    def ble_disconnect(self, p):
        p.disconnect()

    #
    # Given a peripheral handle, populate readings for that peripheral
    #
    def get_readings(self, i):
        readings = dict()
        handle = self.ble_connect(self.waves[i]["addr"])
        if self.waves[i]["version"] == 1:
            readings = self.get_readings_v1(handle)
        elif self.waves[i]["version"] == 2:
            readings = self.get_readings_v2(handle)
        self.ble_disconnect(handle)
        return readings

    def get_readings_v1(self, p):
        readings = dict()
        for s in self.sensors:
            ch = p.getCharacteristics(uuid=s.uuid)[0]
            if ch.supportsRead():
                val = ch.read()
                val = struct.unpack(s.format_type, val)
                if s.name == "DateTime":
                    readings[s.name] = str(datetime(val[0], val[1], val[2], val[3], val[4], val[5]))
                else:
                    readings[s.name] = str(val[0] * s.scale)

        return readings

    def get_readings_v2(self, p):
        readings = dict()

        # The V2 waves return all sensor readings as a single characteristic
        ch = p.getCharacteristics(uuid=UUID("b42e4dcc-ade7-11e4-89d3-123b93f75cba"))[0]
        val = ch.read()
        data = struct.unpack("<4B8H", val)

        if data[0] != 1:
            raise ValueError("Unsupported version from wave device (Expected 1, got{})".format(data[0]))

        readings["DateTime"] = str(datetime.now())
        readings["Temperature"] = str(data[6]/100.0)
        readings["Humidity"] = str(data[1]/2.0)
        readings["Radon-Day"] = str(data[4])
        readings["Radon-Long-Term"] = str(data[5])

        return readings

    def publish_readings(self, name, readings):
        print("name: {0}  readings: {1}".format(name, readings))
        for s in self.sensors:
            topic = "{0}/{1}".format(name, s.name)
            payload = "{0}".format(readings[s.name])
            print("{0} / {1}".format(topic, payload))
            msg_info = self.mqtt_client.publish(topic, payload, retain=False)
            msg_info.wait_for_publish()
            # Mosquitto doesn't seem to get messages published back to back
            time.sleep(0.1)
