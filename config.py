#
#
# Config file for point information  reader

# True  - Running on Pi
# False - Running on PC
IS_RUNNING_ON_PI = False

DISPLAY_POINT_REQUEST_PACKETS_DETAIL   = 1
DISPLAY_POINT_REQUEST_PACKETS_OVERVIEW = 0

PC_COM_PORT = "COM2"
RPI_COM_PORT = "/dev/ttyUSB0"

# Mode to go through each configured loop device and log
# info to USB
POINT_INFO_SCAN = 1
# Checker mode
CHECKER_MODE    = 2

MODE_IS = POINT_INFO_SCAN

# Configurations being brought in from conf.py
# If DEBUG == True, no logging
DEBUG = False

# LED States, solid or blinking, RPi only
curr_state = 'SOLID'
prev_state = ''
state = 'SOLID'
run_cmd = False
cmd = ''

# Logging
LOGPATH = 'logs'
