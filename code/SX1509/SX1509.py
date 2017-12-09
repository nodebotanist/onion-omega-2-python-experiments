from OmegaExpansion import onionI2C

class SX1509:

  REGISTERS = {
    'CHECK': 0x13,
    'RESET': 0x7D,
    'PIN_DIRECTION': 0x0E,
    'PIN_DATA': 0x10,
    'CLOCK': 0x1E,
    'MISC': 0x1F
  }

  def __init__(self, address):
    self.address = address
    self.i2c = onionI2C.OnionI2C()
    self.i2c.setVerbosity(1)

  def start(self):
    registerCheck = self.i2c.readBytes(self.address, self.REGISTERS['CHECK'], 2)
    if not registerCheck == [255, 0]:
      print('SX1509 Not Found')
    self.softReset()

  def softReset(self):
    self.i2c.writeByte(self.address, self.REGISTERS['RESET'], 0x12)
    self.i2c.writeByte(self.address, self.REGISTERS['RESET'], 0x34)
  
  def startInternalClock(self): 
    clockStatus = self.i2c.i2cReadBytes(self.address, self.REGISTERS['CLOCK'], 1)
    miscStatus = self.i2c.i2cReadBytes(self.address, self.REGISTERS['MISC'], 1)
    clockStatus = self.useBitMask(clockStatus, 7, True)
    clockStatus = self.useBitMask(clockStatus, 6, False)
    clockStatus = self.useBitMask(clockStatus, 5, False)
    miscStatus = self.useBitMask(miscStatus, 6, False)
    miscStatus = self.useBitMask(miscStatus, 5, False)
    miscStatus = self.useBitMask(miscStatus, 4, True)
    self.i2c.i2cWrite(self.address, self.REGISTERS['MISC'], miscStatus)
    self.i2c.i2cWrite(self.address, self.REGISTERS['CLOCK'], clockStatus)

  def setPinDirection(self, pin, direction):
    currentPinState = self.i2c.readBytes(self.address, self.REGISTERS['PIN_DIRECTION'], 2)
    bitOn = True
    if direction == 'output':
      bitOn = False
    newPinState = self.useBitMask(currentPinState, pin, bitOn)
    self.i2c.writeBytes(self.address, self.REGISTERS['PIN_DIRECTION'], newPinState)

  def setDigitalPinValue(self, pin, value):
    currentPinState = self.i2c.readBytes(self.address, self.REGISTERS['PIN_DATA'], 2)
    bitOn = True
    if not bitOn == 1:
      bitOn = False
    newPinState = self.useBitMask(currentPinState, pin, bitOn)
    self.i2c.writeBytes(self.address, self.REGISTERS['PIN_DATA'], newPinState)

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

