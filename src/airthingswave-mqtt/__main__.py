from __future__ import print_function
import os,sys
import airthingswave
import time

def usage():
    print("Usage: {0} <config file>".format(sys.argv[0]))

def test():
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
            bqm3, temp, humidity, date = atw.get_reading(atw.waves[iter]["addr"])
            print("{0} says {1}, {2}, {3}, {4}".format(atw.waves[iter]["name"],date, temp, humidity, bqm3))
            iter = iter+1
    return True

test()
