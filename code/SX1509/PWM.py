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

