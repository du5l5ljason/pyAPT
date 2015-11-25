#!/usr/bin/env python
"""
Usage: python home.py [<serial>] [<channel ID>]

This program homes all APT controllers found, or of the one specified
"""
from __future__ import absolute_import
from __future__ import print_function

import time
import pyAPT

from runner import runner_serial

def main(args):
    serial = args[1]
    channelID = args[2]
    print('\tSerial No ', serial)
    print('\tChannel ID', channelID)

    with pyAPT.BSC202(serial_number=serial) as con:
        print('\tIdentifying controller')
        con.identify()
        print('\tHoming parameters:', con.request_home_params(channelID))
        print('\tHoming stage...', end=' ')
        # con.home(velocity = 10)
        print('homed')

if __name__ == '__main__':
  import sys
  sys.exit(main(sys.argv))

