from __future__ import print_function
import os,sys
import airthingswave
import time

def usage():
    print("Usage: {0} <config file>".format(sys.argv[0]))

def main():
    if len(sys.argv) < 2:
        usage()
        return False

    c = sys.argv[1]
    print ("Config file: {0}".format(c))

    atw=airthingswave.AirthingsWave_mqtt(c)

    count=len(atw.waves)
    if count > 0:
        iter=0
        while iter<count:
            print(atw.waves[iter]["name"], atw.waves[iter]["addr"])
            handle = atw.ble_connect(atw.waves[iter]["addr"])
            r = atw.get_readings(handle)
            atw.ble_disconnect(handle)
            print("{0} says Date: {1} Temp: {2} Humidity: {3} 24H: {4} Long term: {5}".format(atw.waves[iter]["name"],r["DateTime"],r["Temperature"], r["Humidity"], r["Radon-Day"], r["Radon-Long-Term"], ))
            atw.publish_readings(atw.waves[iter]["name"], r)
            iter = iter+1
    return True

main()
