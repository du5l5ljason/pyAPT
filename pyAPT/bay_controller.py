from __future__ import absolute_import, division
from .controller import Controller
from . import macros_apt as ENUM
from .message import Message
from . import message

class bay_controller(object):
  """
  In card-slot (bay) systems like BSC20X series, there is only one USB node for a number of sub-modules.
  As a result, all of the bay controllers share one USB device.
  """
  def __init__(self, controller, address):
    super(bay_controller, self).__init__()

    # used for communication
    # self address is the bay address.
    # also let the controller address point to the bay address
    self._address = address
    self._controller = controller
    self._controller._address = self._address

  def address(self):
    return self._address

  def controller(self):
    return self._controller