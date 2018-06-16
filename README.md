# Get Readings from an Airthings Wave and publish to MQTT server

[Airthings](http://airthings.com) makes a BTLE Radon detector called "Wave". This is both an API and a daemon that will periodically publish a a reading to an MQTT server.

## Limitations

```Python
class AirthingsWave:
    def __init__(self, config_file):
```

Class instantiation requires a path to a config file in YAML format.

## API

