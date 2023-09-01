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
MAX_TEMP = 26

# set hysteresis for turning off fan
FINISH_TEMP = MAX_TEMP - 4

# initialize room temp variable
_, room_temp = edgepi_tc.read_temperatures()

FAN_STATE = False

RUN = True
while RUN:
    # wait 1 second between samples
    time.sleep(1)
    # read cold-junction and linearized thermocouple temperatures
    _, room_temp = edgepi_tc.read_temperatures()
    # print room temperature
    print(room_temp)

    # turn on fan if room temp exceeds max temp and fan hasn't already been turned on
    if room_temp > MAX_TEMP and not FAN_STATE:
        print("TOO HOT! Time to cool down!")
        # write voltage value of 10 V to analog out pin number 4
        edgepi_dac.write_voltage(Ch.AOUT4, 7)
        # read state of DAC output 4
        code, voltage, gain = edgepi_dac.get_state(Ch.AOUT4, True, True, True)
        print(code,voltage,gain)
        # Turn fan state on
        FAN_STATE = True

    # turn off fan if room temp is below finish condition
    if room_temp < FINISH_TEMP and FAN_STATE:
        print("Finished Cooling!")
        edgepi_dac.reset()
        # Turn fan state off
        FAN_STATE = False
