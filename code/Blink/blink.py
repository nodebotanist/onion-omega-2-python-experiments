import time
import onionGpio

pin = onionGpio.OnionGpio(3)
on = True

pin.setOutputDirection(0)

while True:
  if on:
    pin.setValue(0)
    on = False
  else:
    pin.setValue(1)
    on = True
  time.sleep(0.5)


