#!/usr/bin/env python
import urllib2
#import commands
import subprocess
import shlex
import time
import datetime
import readID as readIDVar;
#current script
counter = 0;
consecutiveRuns = 0;
timeDelay = 0

pid = readIDVar.readID();
pid = pid.strip()
print("The PI id is " + str(pid))

while(True):
    startTime = datetime.datetime.now();

    readURL = "http://18.130.170.116/service.php?action=r&id=" + str(pid)
    response = urllib2.urlopen(readURL)
    #print(readURL);
    content = response.read();
    counter = counter + 1;
    print("\nLoop "+str(counter));
    print "Packet in jobs list : \n"+content

    if(len(content) > 1):
	consecutiveRuns = 0;
        print(content)
        action = "python /home/pi/packetizer/pointinfotest.py " + content;
        print('*' + action + '*')
        payload = subprocess.check_output(shlex.split(action));
        if len(payload) > 1: #for some reason printing an empty payload still constitutes to greater than 0, so we use 1 instead
            print "Payload response to serviced packet : \n"+payload; 
            reply = "http://18.130.170.116/service.php?action=w&id="+str(pid)+"&payload=" + str(payload)
            #reply = "http://3.8.97.201/service.php?action=w"+"&payload=" + str(payload) +"&id=" +str(pid)
	    #reply = urllib2.quote(reply)
	    print(reply)
            response = urllib2.urlopen(reply)
	else:
	    print("this is the payload" + str(payload))
            print "No device recorded for this point",

    else:
        consecutiveRuns = consecutiveRuns + 1;

    #Currently this condition will assign timeDelay redundantly, should be made more efficient.
    if(consecutiveRuns > 30):
        timeDelay = 1.8;   #sleep for 1.8seconds due to period of inactivity;
    else:
        timeDelay = 0.08;  #if a http request comes in then decrease the delay as we expect further traffic to arrive.

    time.sleep(timeDelay);

    endTime = datetime.datetime.now();
    difference = endTime - startTime;
    difference = (difference.total_seconds() * 1000);

    print("Time taken to run Loop " + str(counter)+ " = " + str(difference));

