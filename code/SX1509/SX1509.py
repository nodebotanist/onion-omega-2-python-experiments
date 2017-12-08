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
    bitmask = 0x0000
    bitmask |= (1 << pin)
    currentPinState = self.i2c.readBytes(self.address, 0x0E, 2)
    newPinState = [0x00, 0x00]
    if direction == 'output':
      bitmask = ~(bitmask)
      bitmaskHighByte = bitmask >> 8
      newPinState[0] = bitmaskHighByte & currentPinState[0]
      newPinState[1] = currentPinState[1] & bitmask
    else:
      bitmaskHighByte = bitmask >> 8
      newPinState[0] = bitmaskHighByte | currentPinState[0]
      newPinState[1] = currentPinState[1] | bitmask
    print(currentPinState)
    print('\n')
    print(newPinState)
    self.i2c.writeBytes(self.address, 0x0E, newPinState)
  def setDigitalPinValue(self, pin, value):
    register = 0x10
    bitmask = 0x0000
    bitmask |= 1 << pin
    currentPinState = self.i2c.readBytes(self.address, register, 2)
    newPinState = [0x00, 0x00]
    if value == 1:
      bitmaskHighByte = bitmask >> 8
      newPinState[0] = bitmaskHighByte | currentPinState[0]
      newPinState[1] = currentPinState[1] | bitmask
    else:
      bitmask = ~(bitmask)
      bitmaskHighByte = bitmask >> 8
      newPinState[0] = bitmaskHighByte & currentPinState[0]
      newPinState[1] = currentPinState[1] & bitmask
    self.i2c.writeBytes(self.address, register, newPinState)