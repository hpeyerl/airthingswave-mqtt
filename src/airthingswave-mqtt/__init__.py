import sys

__version__ = "0.2"

__uri__ = 'https://github.com/hpeyerl/AirthingsWave-mqtt'
__title__ = "AirthingsWave"
__description__ = 'Get readings from an Airthings.com Wave BTLE Radon detector'
__doc__ = __description__ + " <" + __uri__ + ">"
__author__ = 'Herb Peyerl'
__email__ = 'hpeyerl+wave@beer.org'
__license__ = "MIT"

__copyright__ = "Copyright (c) 2017 Herb Peyerl"

from .airthingswave import AirthingsWave_mqtt

if __name__ == '__main__': print(__version__)
