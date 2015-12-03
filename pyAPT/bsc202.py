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

    self._num_modules = 2
    self._address = ENUM.MOTHER_BOARD_ID
    self._module_address = [ENUM.BAY_ID_1, ENUM.BAY_ID_2]
    self.modules = []
    for i in range(self._num_modules):

      state = self.request_bay_used(i)
      if state:
        print "bay", i, "is used!"
        # allocate address
        bay_ctrl = bay_controller(self, self._module_address[i])
        # set channel state - channel 1 on.
        bay_ctrl.controller().set_chanelable_state(channelID = 0x01)
        # set digital output
        bay_ctrl.controller().set_dig_output()
        # set velocity params 0x0413
        bay_ctrl.controller().set_velocity_parameters()
        # set jog params 0x0416

        # set limit switch params 0x0423
        self.modules.append(bay_ctrl)


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
    enccnt = 409600
    T = 2048/6e6

    # these equations are taken from the APT protocol manual
    self.position_scale = enccnt
    self.velocity_scale = enccnt * 53.68
    self.acceleration_scale = 0.01100097656

    self.linear_range = (0,50)

  def numModules(self):
    return self._num_modules

  def request_bay_used(self, bayId = 0x00):
    reqmsg = Message(message.MGMSG_RACK_REQ_BAYUSED,
                              param1 = bayId,
                              dest = self.address())

    self._send_message(reqmsg)
    getmsg = self._wait_message(message.MGMSG_RACK_GET_BAYUSED)

    # print("msgID = %04x, bayID = %02x, state = %02x, dest = %02x, src = %2x" %(getmsg.messageID, getmsg.param1, getmsg.param2, getmsg.dest, getmsg.src))
    return getmsg.param2 == 1

  def set_chanelable_state(self, channelID = 0x00):
    setmsg = Message(message.MGMSG_MOD_SET_CHANENABLESTATE,
                              param1 = channelID,
                              dest = self.address())
    self._send_message(setmsg)

  def request_chanenable_state(self, channelID = 0x00):
    reqmsg = Message(message.MGMSG_MOD_REQ_CHANENABLESTATE,
                              param1 = channelID,
                              dest = self.address())

    self._send_message(reqmsg)
    getmsg = self._wait_message(message.MGMSG_MOD_GET_CHANENABLESTATE)
    print(getmsg)

  def set_dig_output(self):
    setmsg = Message(message.MGMSG_MOD_SET_CHANENABLESTATE,
                              dest = self.address())

    self._send_message(setmsg)



