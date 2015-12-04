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
    numTests = 10
    with pyAPT.BSC202(serial_number=serial) as con:
        numModules = con.numModules()
        if moduleID >= numModules:
            print("Error: moduleID %d is exceeding the number of modules!" % moduleID)
            return 1

        con.route_to_module(moduleID)
        for i in range(numTests):
            status = con.home()
            while status > 0:
                # suspend end of move messages. Resend a move home message.
                print("\tFailed to receive homed message!")
                print("\Resend home message!")
                con.suspend_end_of_move_messages()
                status = con.home()

            print("\tHomed!")
            time.sleep(0.5)
            print('iteration : %d' %i)
        print('\nPress any key to exit!')
        sys.stdin.readline()

if __name__ == '__main__':
  import sys
  sys.exit(main(sys.argv))

