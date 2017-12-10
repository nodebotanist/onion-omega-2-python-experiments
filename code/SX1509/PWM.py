import time
from SX1509 import SX1509

expander = SX1509(0x3E)

expander.start()
expander.startInternalClock()
expander.setDisableInputBuffer(5, True)
expander.setDisableInputBuffer(6, True)
expander.setDisableInputBuffer(7, True)
expander.setPullupResistor(5, False)
expander.setPullupResistor(6, False)
expander.setPullupResistor(7, False)
expander.setPinDirection(5, 'output')
expander.setPinDirection(6, 'output')
expander.setPinDirection(7, 'output')
expander.enableLEDDriver(5, True)
expander.enableLEDDriver(6, True)
expander.enableLEDDriver(7, True)
expander.setDigitalPinValue(5, 0)
expander.setDigitalPinValue(6, 0)
expander.setDigitalPinValue(7, 0)

expander.setPWMPinValue(5, 0x66)
expander.setPWMPinValue(6, 0x33)
expander.setPWMPinValue(7, 0x99)
