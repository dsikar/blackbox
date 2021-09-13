#
#
# Config file for point information  reader

# True  - Running on Pi
# False - Running on PC
IS_RUNNING_ON_PI = True

DISPLAY_POINT_REQUEST_PACKETS_DETAIL   = 0
DISPLAY_POINT_REQUEST_PACKETS_OVERVIEW = 1

PC_COM_PORT = "COM3"
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

# TODO
# We would want something like
# MX5_PACKET_TO_DECODE_LENGTH = 57
# MX6_PACKET_TO_DECOD_LENGTH = 58 # assumed to be different
# then assume a defaulg
# PACKET TO DECODE_LEGNTH = MX5_PACKETT_TO_DECODE_LENGTH
# then at runtime, we could check the standard and reassign if different
# config.PACKET_TO_DECODE_LENGTH = config.MX6_PACKET_TO_DECODE_LENGTH
PACKET_TO_DECODE_LENGTH = 57 
