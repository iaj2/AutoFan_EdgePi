import time
from edgepi.tc.edgepi_tc import EdgePiTC
from edgepi.tc.tc_constants import ConvMode
from edgepi.dac.dac_constants import DACChannel as Ch
from edgepi.dac.edgepi_dac import EdgePiDAC

# Initialize new DAC and Thermocouple
edgepi_dac = EdgePiDAC()
edgepi_tc = EdgePiTC()

# setting DAC range 0-10V
edgepi_dac.set_dac_gain(True)

# set thermocouple to measure temperature continuously
edgepi_tc.set_config(conversion_mode=ConvMode.AUTO)

# set max temp condition
max_temp = 28

# set finished cooling condition
finish_temp = max_temp - 3

# initialize room temp variable
room_temp = edgepi_tc.read_temperatures()[1]

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
    # write voltage value of 10 V to analog out pin number 4
    edgepi_dac.write_voltage(Ch.AOUT4, 10)
    # read state of DAC output 1
    code, voltage, gain = edgepi_dac.get_state(Ch.AOUT4, True, True, True)
    print(code,voltage,gain)
  
  # turn off fan if room temp is below finish condition
  if room_temp < finish_temp and fan_on:
    fan_on = False
    print("Finished Cooling!")
    edgepi_dac.reset()


# stop continuous measurements once you're done sampling
edgepi_tc.set_config(conversion_mode=ConvMode.SINGLE)
