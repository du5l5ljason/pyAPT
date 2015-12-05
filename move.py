#!/usr/bin/env python
"""
Usage: python move.py <serial> <moduleID> <total_dist_mm> <steps>

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
    totalDist = float(args[3])
    steps = int(args[4])
    distPerStep = totalDist / steps
  try:
    with pyAPT.BSC202(serial_number=serial) as con:
      print('Found APT controller S/N',serial)

      con.route_to_module(moduleID)
      con.home()
      con.set_pos_counter()
      con.set_enccounter()
      print('HOMED')
      time.sleep(0.5)
      last_pos = 0
      for i in range(steps):
        print('\tMoving stage by %.2fmm...'%(distPerStep), end=' ')
        status = con.move_rel(dist_mm = distPerStep, start_pos_mm = last_pos)
        print("status = %d" % status)
        while status > 0:
          print('\tFailed to complete move!')
          status = con.move(last_pos + distPerStep)

        print('moved')
        last_pos = last_pos + distPerStep
        print('\tNew position: %.2fmm'%(last_pos))
        time.sleep(0.5)
      return 0
  except pylibftdi.FtdiError as ex:
    print('\tCould not find APT controller S/N of',serial)
    return 1

if __name__ == '__main__':
  import sys
  sys.exit(main(sys.argv))
