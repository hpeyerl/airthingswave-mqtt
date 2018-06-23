# Get Readings from an Airthings Wave and publish to MQTT server

[Airthings](http://airthings.com) makes a BTLE Radon detector called "Wave". This is an executable intended to be called periodically from Cron or some other scheduler to publish readings to an MQTT server.

## Limitations
## API

```Python
class AirthingsWave:
    def __init__(self, config_file):
```

Class instantiation requires a path to a config file in YAML format.
