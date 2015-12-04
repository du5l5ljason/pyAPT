from __future__ import absolute_import, division
from .controller import Controller
from .bay_controller import bay_controller
from . import macros_apt as ENUM
from .message import Message
from . import message

class BSC202(Controller):
  """
  A controller for BSC202, which is a two-channel (or two-module, with single channel for each module) stepper motor controller
  """
  def __init__(self,*args, **kwargs):
    super(BSC202, self).__init__(*args, **kwargs)

    # Check
    # Note that these values are pulled from the APT User software,
    # as they agree with the real limits of the stage better than
    # what the website or the user manual states
    self.max_velocity = 1.0
    self.max_acceleration = 1.0

    # from private communication with thorlabs tech support:
    # steps per revolution: 48
    # gearbox ratio: 256
    # pitch: 0.5 mm
    # thus to advance 1 mm you need to turn 48*256*2 times
    enccnt = 409600.0
    T = 2048/6e6

    # these equations are taken from the APT protocol manual
    self.position_scale = enccnt
    self.velocity_scale = enccnt * 53.68
    self.acceleration_scale = 409600.0 / 90.9

    self.linear_range = (0,50)

    self._num_modules = 2
    self._address = ENUM.MOTHER_BOARD_ID
    self._module_address = [ENUM.BAY_ID_1, ENUM.BAY_ID_2]

    # Start Up
    self.init_notify()
    self._address = ENUM.BAY_ID_1
    self.init_notify()
    self._address = ENUM.BAY_ID_2
    self.init_notify()
    self._address = ENUM.MOTHER_BOARD_ID
    self.modules = []
    for i in range(self._num_modules):

      state = self.request_bay_used(i)
      if state:
        print "bay", i, "is used!"
        # allocate address
        bay_ctrl = bay_controller(self, self._module_address[i])

        # get hw info
        # info = bay_ctrl.controller().info()
        # bay_ctrl.controller().serial_number = info[0]

        # set channel state - channel 1 on.
        bay_ctrl.controller().set_chanelable_state(channelID = ENUM.CHAN_ID_1)
        # set digital output
        bay_ctrl.controller().set_dig_output()
        # set velocity params 0x0413
        bay_ctrl.controller().set_velocity_parameters()
        # set jog params 0x0416

        # set limit switch params 0x0423

        # set power params
        # bay_ctrl.controller().set_power_params()

        # set general move params
        bay_ctrl.controller().set_gen_move_params()

        # set home params
        bay_ctrl.controller().set_home_params()

        # set moverel params

        # set bownindex (skip)

        # start update msgs
        bay_ctrl.controller().start_update_msgs()
        # set joy stick params (skip)
        self.modules.append(bay_ctrl)


  def route_to_module(self, bayId = 0):
    """
    switch the controller pointer to the specific module
    """
    if bayId >= self.numModules():
      return
    else:
      print "BSC202 address", self.address()
      print "submodule address", self.modules[bayId].address()
      self._address = self.modules[bayId].address()


  def numModules(self):
    return self._num_modules




