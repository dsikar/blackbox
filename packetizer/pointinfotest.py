from serialdatatransfer import SerialDataTransfer;
from readers import DataReader;
from byte import Byte;

import sys
import subprocess
import time

tempData = 0;
startTime = 0;
currentTime = 0;

class PointInfoPacketConstruction:

    def createPointInformationPacket(self, data):

      # transfer = SerialDataTransfer("/dev/ttyUSB0");
      # windows variant
      transfer = SerialDataTransfer("COM4");

      varlist = map(int, data.split(','));

      reader   = DataReader(transfer);
      reader.Start();#executes read thread to process incoming response after sent request

      transfer.Write(varlist);
      read(reader,transfer);

def read(reader, transfer):

    startTime = time.time();
    #Responsible for preventing endless rx thread loop
    LoopControl = True;
    strVar = "";
    while(LoopControl):
        data = reader.Read();
	currentTime = time.time();

        if(len(data) == 1):
            if(data[0] == 0x06):
                time.sleep(0.04);
        
                data = reader.Read();
                if(len(data) == 0):
                    LoopControl = False;

        if(len(data) > 1):
            transfer.Write([0x06]);
            for index in range(0, len(data)):
                    item = data[index];
                    strVar += str(Byte(item)) + ',';
            LoopControl = False;

	if((currentTime - startTime) > 5):	#if after 5 seconds has passed and we get stuck in the loop then break out
	    LoopControl = False;

    if(LoopControl == False):
       reader.Stop();
       print(strVar);
       if(reader.IsRunning() == False):
           reader.__del__();
	

if(__name__=='__main__'):

    data = sys.argv[1];
    tempData = data;

    packetObject = PointInfoPacketConstruction();
    packetObject.createPointInformationPacket(data);

    




