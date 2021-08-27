#!/bin/bash
SERVICE="service-loop.py" COM1SERVICE="com-1.py"

if pgrep -f "$SERVICE" >/dev/null 
then
    echo "$SERVICE is running" 
else
    nohup python /home/pi/blackbox/service-loop.py &
    echo "$SERVICE stopped, starting service." 
fi

# NO CABLE TO SPARE AT THE MOMENT
#if pgrep -f "$COM1SERVICE" >/dev/null 
#then
#    echo "$COM1SERVICE is running"
#else
    #nohup python /var/www/html/MXSpeak/packetizer/com-1.py &
#    echo "$COM1SERVICE, starting service." 
#fi

