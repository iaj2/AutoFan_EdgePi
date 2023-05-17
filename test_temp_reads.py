import time
from edgepi.tc.edgepi_tc import EdgePiTC
from edgepi.tc.tc_constants import ConvMode

# initialize thermocouple
edgepi_tc = EdgePiTC()

# set thermocouple to measure temperature continuously
edgepi_tc.set_config(conversion_mode=ConvMode.AUTO)

MAX_TEMP = 28

_,room_temp = edgepi_tc.read_temperatures()

# sample temperature readings until room temp exceeds max temp
while room_temp < MAX_TEMP:
    time.sleep(1)                           # wait 1 second between samples
    _,room_temp = edgepi_tc.read_temperatures()
    print(room_temp)

print("TOO HOT! Time to cool down!")

# stop continuous measurements once you're done sampling
edgepi_tc.set_config(conversion_mode=ConvMode.SINGLE)
