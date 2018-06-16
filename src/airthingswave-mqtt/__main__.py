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
    print(atw.config)

    return True

test()
