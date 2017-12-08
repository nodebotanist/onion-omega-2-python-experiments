import time
from SX1509 import SX1509

expander = SX1509(0x3E)
on = False

expander.start()

expander.setPinDirection(13, 'output')

while True:
  if on:
    expander.setDigitalPinValue(13, 0)
    on = False
  else:
    expander.setDigitalPinValue(13, 1)
    on = True
  time.sleep(0.5)
