'''
*@brief
*  The class is provided for getting the valid packet and published an event if success 
   or block when there is no correct packet received.
*  Input: dataTransfer, Flg (for checking if a response is needed) 
*  Output: received packet.
'''

from LocalFrameFormatter import LocalFrameFormatter;
from readers import DataReader, IDataReader, BadPacketReadError;
from serialdatatransfer import SerialDataTransfer;
from byte import Byte;
from messaging import*;
from frame import*;

class PacketReader(IDataReader,Publisher):

    def __init__(self, dataTransfer):
        self._dataTransfer = dataTransfer;
        self.__reader = DataReader(self._dataTransfer);
        if(self.__reader.IsRunning() != True):
            self.__reader.Start();
            self.__RESPONSE_FLAG = False;

    def Read(self, Flg):
        packet = None;
        while(self.__reader.IsDataAvailable() != True):
            pass;
        dataReceived = self.__reader.Read();

        if(len(dataReceived) == 1):
            print('@PacketReader: ACK is received')
            self.__RESPONSE_FLAG = FLAG(Flg).checkFrameType();
            if(self.__RESPONSE_FLAG):
                #if bit 7 is 0, retrun true, it is an information frame, read is needed
                #if bit 7 is 1, retrun false, it is a control frame, no need read
                packet  = self.Read(Flg);
            else:
                print('@PacketReader: No response is needed');
                packet = None;

        else:
            frame  = LocalFrameFormatter().format(dataReceived);
            lastFrameByte = dataReceived[len(dataReceived)-1];
            if(frame.checksum(frame.packet) == lastFrameByte):
                packet = frame.packet;

                publisher = Publisher();
                publisher.subscribe(PortListener());
                publisher.publish({"@PacketReader: " : 'Data Received Correct'});
                publisher.unsubscribe(PortListener());

                #Print the data received
                for index in range(0 , len(dataReceived)):
                    item  = dataReceived[index];
                    print('D+{0} =  {1}'.format(index, Byte(item)));

            else:
                print('@PacketReader: Data Received Incorrect');
                packet  = self.Read(Flg);

        self._dataTransfer.Write([0x06]);
        self.__reader.Stop();
        return packet;

#Testing Code
if(__name__ == '__main__'):
    dataTransfer = SerialDataTransfer('COM14');
    var = PacketReader(dataTransfer);

    frame = list();
    frame += [1,0,58,228,0,0,0,4,253,146,0,148,0,12,255,0,255,253,254,0,0,1,3,0,0,3,255,255,255,255,255,255,255,255,
              255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,1,127,1,28,208];
    dataTransfer.Write(frame);
    print(frame);

    packet = var.Read(frame[1]); 