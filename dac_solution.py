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
max_temp = 29

# initialize room temp variable
room_temp = edgepi_tc.read_temperatures()[1]

# sample temperature readings until room temp exceeds max temp
while room_temp < max_temp:
  time.sleep(1)                           # wait 1 second between samples
  temps = edgepi_tc.read_temperatures()   # read cold-junction and linearized thermocouple temperatures
  room_temp = edgepi_tc.read_temperatures()[1]
  print(temps)

print("TOO HOT! Time to cool down!")

# write voltage value of 10 V to analog out pin number 4
edgepi_dac.write_voltage(Ch.AOUT4, 9.99)

# read state of DAC output 1
code, voltage, gain = edgepi_dac.get_state(Ch.AOUT4, True, True, True)

print(code,voltage,gain)

# stop continuous measurements once you're done sampling
edgepi_tc.set_config(conversion_mode=ConvMode.SINGLE)

input("Press enter to stop")

# Stop voltage out
edgepi_dac.reset()