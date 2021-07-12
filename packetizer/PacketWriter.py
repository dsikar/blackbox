'''
*@brief
*  The class is provided for writing a packet.
*  Input: dataTransfer, packet, flagbyte
'''
from frame import Frame;   

class PacketWriter:
    def __init__(self, dataTransfer):
        self._dataTransfer = dataTransfer;
        
    def Write(self, packet, flagbyte):
        self._frame    =  Frame(packet, flagbyte);
        self._dataTransfer.Write(self._frame.getByteArray());
        print self._frame.getByteArray();

    def returnFlag(self):
        flag = self._frame.getByteArray()[1];
        return flag;
