#!/usr/bin/env python
import urllib2
#import commands
#import subprocess
#import shlex
import time
import re

from serialdatatransfer import SerialDataTransfer;
from readersBackup import DataReader;

def readerFunction(reader, transfer):

    consecutiveRuns = 0;
    storedData = "";

    while(True):
        try:
	    time.sleep(0.01);
            data = reader.Read();
	    if(len(data) > 0): #if we have data
		#if(data.isspace() == False): #and that data is not a whitespace(logic needs to be modified)
                storedData += data; #Simple appending to existing string is occurring
		consecutiveRuns = 0;
	    else:
	        consecutiveRuns = consecutiveRuns + 1;

	    if(consecutiveRuns > 30):

		if not str(storedData):
	            print("Nothing received from panel after 30 attempts");
		else:
		    result = re.sub(' {2,}',' ',str(storedData));
		    #print(result);
	            #temp = "http://3.9.146.52/com-1-service.php?action="+str(result);
		    #print(temp);
		    result = result.strip();
		    result = urllib2.quote(result);
                    urllib2.urlopen("http://18.135.17.6/com-1-service.php?action="+str(result))
		    #print(storedData);
		storedData = "";
		time.sleep(2);
		consecutiveRuns = 0; 
        except Exception as err:
            print err;


if(__name__ == '__main__'):

    #portname, baudrate, timeout as per serialdatatransfer.ph
    transfer = SerialDataTransfer("/dev/ttyUSB1", 9600);
    reader  = DataReader(transfer);
    reader.Start();

    readerFunction(reader,transfer);
