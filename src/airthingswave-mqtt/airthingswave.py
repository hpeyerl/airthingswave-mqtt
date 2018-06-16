import yaml
import logging

class AirthingsWave_mqtt:
    def __init__(self, config_file):
	with open(config_file, 'r') as f:
		self.config=yaml.load(f)
