# Logging utility functions
import subprocess
import config as conf
import os
import time


def checkLogDir() :
    """
    Check if log direction exists, as defined in config.py
    """
    import os
    import config as conf

    if(os.path.isdir(conf.LOGPATH) == True) :
        print('Logging to {} directory'.format(conf.LOGPATH))
    else :
        print('Directory {} does not exist, creating...'.format(conf.LOGPATH))
        os.mkdir(conf.LOGPATH)


def writelog(entry, logfile) :
    """
    writelog - decided if we are logging on Windows or RPi, then call
    the correct function, pre-pending time and date to log entry
    Input
        entry: string, log entry
        logfile: string, log file
    Output
        none
    """
    curr_time = time.strftime('%d/%m/%Y,%H:%M:%S,', time.gmtime())
    entry = curr_time + entry
    if (conf.IS_RUNNING_ON_PI == False) :
        writelog_windows(entry, logfile)
    else :
        writelog_pi(entry, logfile)


def writelog_windows(entry, logfile) :
    """
    writelog_windows - prepend time and write log entry to log file
    to usb drive is exists, otherwise to /tmp
    Input
        entry: string, log entry
        logfile: string, log file
    Output
        none
    """
    if conf.DEBUG == False:
        logdrive = conf.LOGPATH + '/' + logfile
        fout = open(logdrive, 'a')
        fout.write(entry)
        fout.close()

def writelog_pi(entry, logfile) :
    """
    writelog - write log entry to log file
    to usb drive is exists, otherwise to /tmp,
    setting LED to blinking or solid to reflect
    the action.
    Input
        entry: string, log entry
        logfile: string, log file
    Output
        none
    """
    # where to log
    logdrive = ''
    cnmd = ''
    out = subprocess.check_output(['ls', '/media/pi'])

    if len(out) > 0 :
        logdrive = '/media/pi/' + out
        logdrive = logdrive.rstrip('\n')
        logdrive += '/'
        conf.state = 'BLINKING'
    else :
        logdrive = conf.LOGPATH + '/'
        conf.state = 'SOLID'

    if(conf.prev_state != conf.state) :
        conf.run_cmd = True
        if conf.state == 'SOLID' :
            conf.cmd = 'sudo bash -c \'echo none > /sys/class/leds/led0/trigger\''
        else : # BLINKING
            conf.cmd = 'sudo bash -c \'echo heartbeat > /sys/class/leds/led0/trigger\''
        conf.prev_state = conf.state

    if conf.run_cmd == True :
        #process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        #output, error = process.communicate()
        #print("output: ", output)
        #print("error: ", error)
        conf.run_cmd = False
        os.system(conf.cmd)
        # os.system(cmd)

    logdrive += logfile

    if conf.DEBUG == False :
        fout = open(logdrive, 'a')
        fout.write(entry)
        fout.close()
