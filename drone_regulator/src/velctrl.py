from geometry_msgs.msg import Twist

""" Usage:
      The user calls ready() to check if a new action can be applied. If so a new turn(...) may be issued. The user always calls
      next() which steps the control. If this call returns True then a new value shall be applied to the engine. The user the calls
      val() to get the value.
"""

class Step:
  """ This engine control sends steps """
  def __init__(self):
    self.period = 2
    self.counter = 0
    self.value = 0
    self.ret = 0

  """ Returns true if the control is ready for a new action. This happens at the end of each period. """
  def ready(self):
     return self.counter == 0

  """ Accepts a positive or negative turn and which sets the step size based on
      the absolute value of the input. Zero means stop.
      Note: On a stop the step size is reset to 1 in order to toggle ready as frequently as possible. <--- OK?
  """
  def act(self, val):
    if self.ready(): # Note: self.counter is already zero since ready.
      if val == 0:
        self.value = 0
        self.period = 2
      else :
        self.period = abs(val)*2
        if val > 0:
          self.value = 1
        else:
          self.value = -1

  """ Returns true if a value shall be applied to the engine. Low (i.e. stop) is only sent once but will stay low until next period. """
  def next(self):
    r = False
    self.counter += 1
    if self.value != 0:
      steplen = self.period/2
      if self.counter < steplen+1:
        self.ret = self.value
        r = True 
      elif self.counter == steplen+1:
        self.ret = 0
        r = True

    if self.counter == self.period:
      self.counter = 0

    return r

  def val(self):
    return self.ret

class Pulse:
  """ This engine control sends pulses """
  def __init__(self, width, period, delay):
    self.width = width
    self.delay = delay
    self.period = period
    self.counter = 0
    self.value = 0
    self.ret = 0

  """ Returns true if the control is ready for a new action. This happens at the end of each period. """
  def ready(self):
     return self.delay == 0 and self.counter == 0

  """ Accepts a positive or negative turn and which sets the step size based on
      the absolute value of the input. Zero means stop.
      Note: On a stop the step size is reset to 1 in order to toggle ready as frequently as possible. <--- OK?
  """
  def act(self, val):
#    if self.ready(): # Note: self.counter is already zero since ready.
    if val == 0:
      self.value = 0
    else :
      if val > 0:
        self.value = 1
      else:
        self.value = -1

  """ Returns true if a value shall be applied to the engine. Low (i.e. stop) is only sent once but will stay low until next period. """
  def next(self):
    if self.delay != 0:
      self.delay -= 1
    else:
      r = False
      self.counter += 1
      if self.value != 0:
        if self.counter <= self.width:
          self.ret = self.value
          r = True 
#        elif self.counter == steplen+1:
#          self.ret = 0
#          r = True

      if self.counter == self.period:
        self.counter = 0

      return r

  def val(self):
    return self.ret



class Cont:
  """ This engine control simply sends a continous stream until it is stopped """
  def __init__(self):
     self.value = 0
     self.stop = False

  """ Always ready """
  def ready(self):
     return True

  """ Accepts a positive or negative turn. Zero means stop.  """
  def act(self, val):
    if val > 0:
      self.value = 1
    elif val < 0:
      self.value = -1
    else:
      self.stop = True
      self.value = 0

  """ Returns true if a value shall be applied to the engine. Low (i.e. stop) is only sent once. """
  def next(self):
    return self.value != 0 or self.stop

  def val(self):
    self.stop = False
    return self.value


