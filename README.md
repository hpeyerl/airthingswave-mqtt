# Get Readings from an Airthings Wave and publish to MQTT server

[Airthings](http://airthings.com) makes a BTLE Radon detector called "Wave". This is an executable intended to be called periodically from Cron or some other scheduler to publish readings to an MQTT server.

## Limitations

This application doesn't implement 'find' as provided in the example at https://airthings.com/raspberry-pi/

This is just a python API with a main loop that I happen to use in my own Home-Assistant setup. If you're looking for a plug and play solution, consider [balena-airthingswave](https://github.com/renemarc/balena-airthingswave) - @renemarc has created his appliance package using airthingswave-mqtt.

## API

```Python
class AirthingsWave:
    def __init__(self, config_file):
```

Class instantiation requires a path to a config file in YAML format.

```
mqtt:
  broker: 192.168.30.18
  port: 1883
  username: 
  password: 

waves:
  - name: "basement-radon"
    addr: 98:07:2d:43:4d:ff
```

Before taking a reading, you should:

```
def ble_connect(self, addr):
```

Then you can:

```
def get_readings(self, p):
def publish_readings(self, name, readings):
```

## Example

From \__main\__.py:
```python
c = sys.argv[1]

atw = airthingswave.AirthingsWave_mqtt(c)

count = len(atw.waves)
if count > 0:
    i = 0
    while i < count:
        handle = atw.ble_connect(atw.waves[i]["addr"])
        r = atw.get_readings(handle)
        atw.ble_disconnect(handle)
        atw.publish_readings(atw.waves[i]["name"], r)
        i = i+1

return True
```

## Installation Instructions
The instructions below are for Raspbian on a Raspberry Pi Zero W (but could be modified to support any bluetooth equipped Raspberry Pi or Debian based environment)

1. Setup your RPi Zero W w/ Raspbian Stretch Lite

**Note:** Python 2.7, PIP and Bluez are pre-installed.  If you are using another environment, these dependencies must be installed.

2. Follow the instructions at Airthings ( https://airthings.com/raspberry-pi/ ) to be able to "find" & "read" your Airthings Wave with your RPi Zero W.  Make sure you can "find" and then "read" your Airthings Wave.  Keep the MAC address you use to "read", you'll need it later.

3. Install airthingswave-mqtt on the RPi Zero W
   
   ```
   pip install airthingswave-mqtt
   pip install pyyaml
   ```

4. Create a yaml configuration file for airthingswave-mqtt on the RPi Zero W, we'll call it airthingsconfig.yaml
   
   ```shell
   nano /home/pi/airthingsconfig.yaml
   ```

**Note:** This is in Raspbian's Home Directory (~), but you can place this wherever you want. Include the config below with your details and the MAC address recorded in Step 2.

```
mqtt:
  broker: xxx.xxx.xxx.xxx
  port: 1883
  username: "YOURMQTTUSERNAME"
  password: "YOURMQTTPASSWORD"

waves:
  - name: "radon"
    addr: "cc:78:ab:00:00:00"
```
**Note:**

**Username:** Keep the quotes used above for "YOURMQTTUSERNAME", otherwise it will error out with "has no len ()"

**Password:** Keep the quotes used above for "YOURMQTTPASSWORD", otherwise it will error out with "has no Len ()"

**Name:** Keep the quotes used above, "name it whatever you want", for this example, we used "radon"

**Addr:** This is the MAC recorded earlier. It shouldn't matter, but recommend keeping the letters lowercase. Again, keep the quotes!

5. Try running it with the command
   
   ```shell
    python -m airthingswave-mqtt /home/pi/airthingsconfig.yaml
   ```

If you are successful, you'll see it search and find your Airthings Wave, and report Radon, Radon Long Term, Temperature, Humidity.

6. Now to make sure Home Assistant is setup properly to receive these MQTT messages, add the following to your HA configuration.yaml

```
sensor 1:
  platform: mqtt
  name: "Radon 24HRS"
  state_topic: "radon/Radon-Day"
  unit_of_measurement: "pCi/L"

sensor 2:
  platform: mqtt
  name: "Radon LifeTime"
  state_topic: "radon/Radon-Long-Term"
  unit_of_measurement: "pCi/L"

sensor 3:
  platform: mqtt
  name: "Temperature"
  state_topic: "radon/Temperature"
  unit_of_measurement: "°C"

sensor 4:
  platform: mqtt
  name: "Humidity"
  state_topic: "radon/Humidity"
  unit_of_measurement: "%"
```
**Note:** replace "radon" with whatever you chose to name it.

7. Before restarting your HA, it is recommended that you watch Home Assistant and make sure the MQTT messages are properly received by enabling the following in your HA configuration.yaml.  Once you've validated everything is working, you can Disable/Remove this from your config.

```
logger:
  default: warning
  logs:
    homeassistant.components.mqtt: debug
```

8. tail your HA log file

```shell
    tail -f home-assistant.log
   ```

9. Restart your HA

10. Issue the command in Step 5 on your RPi Zero W, if all is working you should see HA listening on the MQTT instances you created and successful reports coming in from your RPi Zero W

11. Once everything is working, set the Step 5 command as a cron job and remove the logging function from HA in Step 7
