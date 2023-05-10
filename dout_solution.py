import time
from edgepi.gpio.gpio_constants import GpioPins
from edgepi.digital_output.edgepi_digital_output import EdgePiDigitalOutput
from edgepi.tc.edgepi_tc import EdgePiTC
from edgepi.tc.tc_constants import ConvMode

# Initialize new Thermocouple and DOUT
edgepi_tc = EdgePiTC()
edgepi_dout = EdgePiDigitalOutput()

# set thermocouple to measure temperature continuously
edgepi_tc.set_config(conversion_mode=ConvMode.AUTO)

# set max temp condition
max_temp = 28

# set finished cooling condition
finish_temp = max_temp - 3

# initialize room temp variable
room_temp = edgepi_tc.read_temperatures()[1]

# Check if fan is off/on
fan_on = False

run = True
while run:
  # wait 1 second between samples
  time.sleep(1)             
  # read cold-junction and linearized thermocouple temperatures
  temps = edgepi_tc.read_temperatures()       
  room_temp = edgepi_tc.read_temperatures()[1]
  print(temps)
  
  # turn on fan if room temp exceeds max temp and fan hasn't already been turned on
  if room_temp > max_temp and not fan_on:
    fan_on = True
    print("TOO HOT! Time to cool down!")
    # setting GpioPin 4 to output direction
    edgepi_dout.digital_output_direction(GpioPins.DOUT4, False)
    # setting GpioPin 4 to High/On
    edgepi_dout.digital_output_state(GpioPins.DOUT4, True)
  
  # turn off fan if room temp is below finish condition
  if room_temp < finish_temp and fan_on:
    fan_on = False
    print("Finished Cooling!")
    # setting GpioPin 4 to Low/Off
    edgepi_dout.digital_output_state(GpioPins.DOUT4, False)


# stop continuous measurements once you're done sampling
edgepi_tc.set_config(conversion_mode=ConvMode.SINGLE)
