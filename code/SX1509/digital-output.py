from SX1509 import SX1509

expander = SX1509(0x3E)

expander.start()

expander.setPinDirection(3, 'output')
expander.setPinDirection(3, 'input')

