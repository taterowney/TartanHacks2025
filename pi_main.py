from vision import *
from serialcomms.serial_pi import pi_mainloop

if __name__ == '__main__':
    pi_mainloop(port="/dev/serial0")
