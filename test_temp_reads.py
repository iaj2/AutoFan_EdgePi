import time
from edgepi.tc.edgepi_tc import EdgePiTC
from edgepi.tc.tc_constants import ConvMode

# initialize thermocouple
edgepi_tc = EdgePiTC()

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

# stop continuous measurements once you're done sampling
edgepi_tc.set_config(conversion_mode=ConvMode.SINGLE)