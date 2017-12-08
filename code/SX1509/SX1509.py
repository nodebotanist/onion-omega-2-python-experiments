from OmegaExpansion import onionI2C

class SX1509:
  def __init__(self, address):
    self.address = address
    self.i2c = onionI2C.OnionI2C()
    self.i2c.setVerbosity(1)
  def start(self):
    registerCheck = self.i2c.readBytes(self.address, 0x13, 2)
    if not registerCheck == [255, 0]:
      print('SX1509 Not Found')
    self.softReset()
  def softReset(self):
    self.i2c.writeByte(self.address, 0x7D, 0x12)
    self.i2c.writeByte(self.address, 0x7D, 0x34)
  def setPinDirection(self, pin, direction):
    register = 0x0E
    currentPinState = self.i2c.readBytes(self.address, 0x0E, 2)
    bitOn = True
    if direction == 'output':
      bitOn = False
    newPinState = self.useBitMask(currentPinState, pin, bitOn)
    self.i2c.writeBytes(self.address, register, newPinState)
  def setDigitalPinValue(self, pin, value):
    register = 0x10
    currentPinState = self.i2c.readBytes(self.address, register, 2)
    bitOn = True
    if not bitOn == 1:
      bitOn = False
    newPinState = self.useBitMask(currentPinState, pin, bitOn)
    self.i2c.writeBytes(self.address, register, newPinState)
  def useBitMask(self, currentState, bit, bitOn):
    mask = [0x00, 0x00]
    maskBase = 0x0000
    maskBase |= (1 << bit)
    if not bitOn:
      maskBase = ~maskBase
    highByte = maskBase >> 8
    if bitOn:
      mask[0] = currentState[0] | highByte
      mask[1] = currentState[1] | maskBase
    else:
      mask[0] = currentState[0] & highByte
      mask[1] = currentState[1] & maskBase
    return mask