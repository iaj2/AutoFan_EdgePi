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
MAX_TEMP = 28

# set hysteresis for turning off fan
FINISH_TEMP = MAX_TEMP - 4

# Check if fan is off/on
FAN_STATE = False

RUN = True
while RUN:
    # wait 1 second between samples
    time.sleep(1)
    # read cold-junction and linearized thermocouple temperatures
    _, room_temp = edgepi_tc.read_temperatures()
    # print room temperature
    print(f"{room_temp} degrees Celsius")

    # turn on fan if room temp exceeds max temp and fan hasn't already been turned on
    if room_temp > MAX_TEMP and not FAN_STATE:
        print("TOO HOT! Time to cool down!")
        # setting GpioPin 4 to output direction
        edgepi_dout.digital_output_direction(GpioPins.DOUT4, False)
        # setting GpioPin 4 to High/On
        edgepi_dout.digital_output_state(GpioPins.DOUT4, True)
        # turn fan state on
        FAN_STATE = True

    # turn off fan if room temp is below finish condition
    if room_temp < FINISH_TEMP and FAN_STATE:
        print("Finished Cooling!")
        # setting GpioPin 4 to Low/Off
        edgepi_dout.digital_output_state(GpioPins.DOUT4, False)
        # turn fan state off
        FAN_STATE = False
