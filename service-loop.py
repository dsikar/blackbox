import subprocess
import shlex
import time
import datetime
import readID as readIDVar

def writelog(entry, logfile) :
    """
    writelog - write log entry to log file
    to usb drive is exists, otherwise to /tmp
    Input
        entry: string, log entry
        logfile: string, log file
    Output
        none
    """
    logdrive = ''
    out = subprocess.check_output(['ls', '/media/pi'])
    if len(out) > 0 :
        logdrive = '/media/pi/' + out
        logdrive = logdrive.rstrip('\n')
        logdrive += '/'
    else :
        logdrive = '/tmp/'
    logdrive += logfile
    fout = open(logdrive, 'a')
    fout.write(entry)
    fout.close()

timeDelay = 1

pid = readIDVar.readID();
pid = pid.strip()
entry = "Logging Panel PI id: " + str(pid) + '\nTODO scan devices, decode packets\n'
print(entry)
f = open('packet.txt')
packets = f.readlines()

logfile = str(datetime.datetime.today().strftime('%Y%m%d%H%M%S'))
logfile += '_BlackBox.log'
# todo, adapt for Windows
print(entry)
# writelog(entry, logfile)

while(True):

    for packet in packets :
        startTime = datetime.datetime.now();

        content =  packet #+ '\r\n' #.strip()
        # print "Packet in jobs list : \n"+content

        action = "python packetizer/pointinfotest.py " + content;
        #print(action)
        payload = subprocess.check_output(shlex.split(action));
        if len(payload) > 1: #for some reason printing an empty payload still constitutes to greater than 0, so we use 1 instead
            # writelog(payload,logfile)
            # TODO adjust to windows 7/10
            print(payload)
            #print "Payload response to serviced packet : \n"+payload; 
	else:
	    #print("this is the payload" + str(payload))
            print "No device recorded for this point",

        time.sleep(timeDelay) 
