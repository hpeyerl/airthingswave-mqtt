from __future__ import print_function
import sys
from . import airthingswave


def usage():
    print("Usage: {0} <config file>".format(sys.argv[0]))


def main():
    if len(sys.argv) < 2:
        usage()
        return False

    c = sys.argv[1]
    print ("Config file: {0}".format(c))

    atw = airthingswave.AirthingsWave_mqtt(c)

    count = len(atw.waves)
    if count > 0:
        i = 0
        while i < count:
            print(atw.waves[i]["name"], atw.waves[i]["addr"])
            handle = atw.ble_connect(atw.waves[i]["addr"])
            r = atw.get_readings(handle)
            atw.ble_disconnect(handle)
            print("{0} says Date: {1} Temp: {2} Humidity: {3} 24H: {4} Long term: {5}".format(atw.waves[i]["name"], r["DateTime"], r["Temperature"], r["Humidity"], r["Radon-Day"], r["Radon-Long-Term"], ))
            atw.publish_readings(atw.waves[i]["name"], r)
            i = i+1

    return True


main()
