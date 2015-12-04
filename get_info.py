#!/usr/bin/env python
"""
Usage: python get_info.py [<serial>]

Gets the  controller information of all APT controllers, or the one specified
"""
from __future__ import absolute_import
from __future__ import print_function

import pyAPT
from pyAPT import BSC202
from pyAPT import bay_controller
from pyAPT import macros_apt as macros
from runner import runner_serial
import sys

@runner_serial
def info(serial):

  addr_list = [macros.MOTHER_BOARD_ID, macros.BAY_ID_1, macros.BAY_ID_2]
  with pyAPT.BSC202(serial_number=serial) as con:

        #info = con.info()
        # print('\tController info:')
        # labels=['S/N','Model','Type','Firmware Ver', 'Notes', 'H/W Ver',
        #         'Mod State', 'Channels']

        # for idx,ainfo in enumerate(info):
        #   print('\t%12s: %s'%(labels[idx], bytes(ainfo)))
        id = 0
        con.route_to_module(id)
        con.home()
        print('\n>>>>Press enter to continue')
        sys.stdin.readline()
        # numModules = con.numModules()
        # for i in range(numModules):
        #   con.route_to_module(i)

if __name__ == '__main__':
  import sys
  sys.exit(info())



