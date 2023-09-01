from edgepi.dac.dac_constants import DACChannel as Ch
from edgepi.dac.edgepi_dac import EdgePiDAC

# initialize DAC
edgepi_dac = EdgePiDAC()

# setting DAC range 0-10V
edgepi_dac.set_dac_gain(True)

# write voltage value of 10 V to analog out pin number 4
edgepi_dac.write_voltage(Ch.AOUT4, 0)

# read state of DAC output 4
code, voltage, gain = edgepi_dac.get_state(Ch.AOUT4, True, True, True)

print(code,voltage,gain)

