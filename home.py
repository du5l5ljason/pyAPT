#!/usr/bin/env python
"""
Usage: python home.py [<serial>] [<moduleID>]

This program homes all APT controllers found, or of the one specified
"""
from __future__ import absolute_import
from __future__ import print_function

import time
import pyAPT
import serial
from runner import runner_serial

def main(args):
    serial = args[1]
    moduleID = int(args[2])

    with pyAPT.BSC202(serial_number=serial) as con:
        numModules = con.numModules()
        if moduleID >= numModules:
            print("Error: moduleID %d is exceeding the number of modules!" % moduleID)
            return 1

        con.route_to_module(moduleID)
        con.home()
        print('\n>>>>HOMED! Press any key to exit!')
        sys.stdin.readline()

if __name__ == '__main__':
  import sys
  sys.exit(main(sys.argv))

