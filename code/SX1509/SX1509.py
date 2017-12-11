from OmegaExpansion import onionI2C

class SX1509:

  REGISTERS = {
    'CHECK': 0x13,
    'RESET': 0x7D,
    'PIN_DIRECTION': 0x0E,
    'PIN_DATA': 0x10,
    'CLOCK': 0x1E,
    'MISC': 0x1F,
    'DISABLE_INPUT_BUFFER': 0x00,
    'PULLUP_RESISTORS': 0x06,
    'LED_DRIVER': 0x20,
    'PWM_INTENSITY': [0x2A, 0x2D, 0x30, 0x33, 0x36, 0x3B, 0x40, 0x45, 0x4A, 0x4D, 0x50, 0x53, 0x56, 0x5B, 0x60, 0x65]
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
    clockStatus = self.i2c.readBytes(self.address, self.REGISTERS['CLOCK'], 1)
    clockStatus = [0x00, clockStatus[0]]
    miscStatus = self.i2c.readBytes(self.address, self.REGISTERS['MISC'], 1)
    miscStatus = [0x00, miscStatus[0]]
    clockStatus = self.useBitMask(clockStatus, 5, False)
    clockStatus = self.useBitMask(clockStatus, 6, True)
    miscStatus = self.useBitMask(miscStatus, 6, False)
    miscStatus = self.useBitMask(miscStatus, 5, False)
    miscStatus = self.useBitMask(miscStatus, 4, True)
    self.i2c.writeByte(self.address, self.REGISTERS['MISC'], miscStatus[1])
    self.i2c.writeByte(self.address, self.REGISTERS['CLOCK'], clockStatus[1])

  def setDisableInputBuffer(self, pin, disableInputBuffer):
    disableInputBufferStatus = self.i2c.readBytes(self.address, self.REGISTERS['DISABLE_INPUT_BUFFER'], 2)
    disableInputBufferStatus = self.useBitMask(disableInputBufferStatus, pin, disableInputBuffer)
    self.i2c.writeBytes(self.address, self.REGISTERS['DISABLE_INPUT_BUFFER'], disableInputBufferStatus)
  
  def setPullupResistor(self, pin, pullupResistorOn):
    pullupResistorStatus = self.i2c.readBytes(self.address, self.REGISTERS['PULLUP_RESISTORS'], 2)
    pullupResistorStatus = self.useBitMask(pullupResistorStatus, pin, pullupResistorOn)

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

  def enableLEDDriver(self, pin, LEDDriverOn):
    ledDriverState = self.i2c.readBytes(self.address, self.REGISTERS['LED_DRIVER'], 2)
    ledDriverState = self.useBitMask(ledDriverState, pin, LEDDriverOn)
    self.i2c.writeBytes(self.address, self.REGISTERS['LED_DRIVER'], ledDriverState)

  def setPWMPinValue(self, pin, value):
    byteValue = 0xFF & value
    self.i2c.writeByte(self.address, self.REGISTERS['PWM_INTENSITY'][pin], byteValue)

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

