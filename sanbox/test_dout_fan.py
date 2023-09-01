import time
from edgepi.gpio.gpio_constants import GpioPins
from edgepi.digital_output.edgepi_digital_output import EdgePiDigitalOutput

# initialize DOUT
edgepi_dout = EdgePiDigitalOutput()

# set GpioPin 4 to OUT direction
edgepi_dout.digital_output_direction(GpioPins.DOUT4, False)

# set Gpiopin 4 to High/on
edgepi_dout.digital_output_state(GpioPins.DOUT4, True)

time.sleep(10)

# set Gpiopin 4 to High/on
edgepi_dout.digital_output_state(GpioPins.DOUT4, False)
