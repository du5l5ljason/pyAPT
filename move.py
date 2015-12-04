#!/usr/bin/env python
"""
Usage: python move.py <serial> <moduleID> <total_distance_mm> <steps>

This program tells the specified controller to move the stage by the specified
distance in mm
"""
from __future__ import absolute_import
from __future__ import print_function

import time
import pylibftdi
import pyAPT

def main(args):
  if len(args)<5:
    print(__doc__)
    return 1
  else:
    serial = args[1]
    moduleID = int(args[2])
    dist = float(args[3])
    steps = int(args[4])
    distPerStep = dist / steps
  try:
    with pyAPT.BSC202(serial_number=serial) as con:
        print('Found APT controller S/N',serial)
        numModules = con.numModules()
        if moduleID >= numModules:
            print("Error: moduleID %d is exceeding the number of modules!" % moduleID)
            return 1

        con.route_to_module(moduleID)
        status = con.home()
        while status > 0:
            # suspend end of move messages. Resend a move home message.
            print("\tFailed to receive homed message!")
            print("\Resend home message!")
            con.suspend_end_of_move_messages()
            status = con.home()

        print("\tHomed!")

        for i in range(steps):
          print('\tMoving stage by %.2fmm...'%(distPerStep), end=' ')
          status = con.move(distPerStep)
          while status > 0:
              # suspend end of move messages. Resend a move home message.
              print("\tFailed to receive move completed message!")
              print("\Resend move message!")
              con.suspend_end_of_move_messages()
              status = con.move(distPerStep)
          print('moved')
          print('\tNew position: %.2fmm'%(con.position()))
        return 0
  except pylibftdi.FtdiError as ex:
    print('\tCould not find APT controller S/N of',serial)
    return 1

if __name__ == '__main__':
  import sys
  sys.exit(main(sys.argv))

