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
    self._controller = controller
    self._controller._address = address

  def address(self):
    return self._controller._address

  def controller(self):
    return self._controller