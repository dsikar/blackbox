"""*********************************************************************************
*  @author (Obaro)
*  @date   (07 September 2018).
*  @description
*   The file contains the implementation of the PTP frame data link layer.
*********************************************************************************"""

from  packet  import Packet;
from  header   import LocalHeader, NetworkHeader, LOCAL_HEADER, NETWORK_HEADER;    

from byte import Byte;

SOH           = 0x01
FLG           = 0x00 
ACK           = 0x06
MODULO        =  256


"""
The PTP Frame
"""
class Frame:

    def __init__(self, packetObject, flgbyte):
        if(isinstance(packetObject, Packet)) != True:
             raise ValueError("@Require parameter one to be a packet object");

        self.__packet         =  packetObject;
        self.__flgbyte          =  flgbyte;
        pass;

    """*****************************************
    * @brief
    *  The function will prepare and get the bytes array 
    *****************************************"""
    def getByteArray(self):
        bytes   =  list();
        bytes   += [SOH, FLAG(self.__flgbyte).FlagSequNum(), self.__packet.size];
        bytes   += self.__packet.getByteArray();
        bytes   += [self.checksum(self.__packet)];
        return bytes;

    @property
    def packet(self):
        return self.__packet;

    def setContent(self, key, value):
       if(isinstance(key , basestring)):
           self.__packet.content.setParameter(key, value);

    def setHeader(self, key, value):
          if(isinstance(key , basestring)):
              self.__packet.header.setParameter( key, value);
   
    def count(self):
        bytes  =  self.getByteArray();
        return len(bytes);

    def checksum(self, packet):
        global MODULO;
        if(isinstance(packet, Packet) != True):
            raise AttributeError("@DataCheckable : Parameter must be a type packets.Packet");
        if (self.__flgbyte == None):
            self.__flgbyte = FLG;
        tempFLG = FLAG(self.__flgbyte).FlagSequNum();
        checksum =  0       
        sum    = int(tempFLG);
        sum    += packet.size;
        bytes  =  packet.getByteArray();

        for data in bytes:
            sum   += data
        checksum   = sum % MODULO;
        return checksum;

'''
*@brief
*  The class is provided for setting&checking flag byte in frame which is 
    used for multiple packets send and determine if a response is needed.
*  Input: flgbyte, FrameType
*  Output: new flag byte
'''
class FLAG:
    def __init__(self, flgbyte):
        self._flgbyte = flgbyte;
        self.__flgbyteList = [];
        self.__flgbyteList = Byte(flgbyte).bitList(flgbyte, 8);

    def checkFrameType(self):   # if bit 7 is 0, it is an information frame
        if (self.__flgbyteList[0] == 0):
            return True;
        else:
            return False;

    def setFrameType(self, FrameType): # true for information frame, false for control frame
        if (FrameType == True):
            self.__flgbyteList[0] = 0;
        else:
            self.__flgbyteList[0] = 1;
        newFLG = Byte(self._flgbyte).integer(self.__flgbyteList);
        return newFLG;

    def FlagSequNum(self):
        tempFLGbitList = [];
        for idx in range(4, 8):
            tempFLGbitList.append(self.__flgbyteList[idx]);
        newFLG = Byte(self._flgbyte).integer(tempFLGbitList);
        return newFLG;

    def increaseFrameFlag(self):
        tempFLGbitList = [];
        for idx in range(4, 8):
            tempFLGbitList.append(self.__flgbyteList[idx]);
        newFLG = Byte(self._flgbyte).integer(tempFLGbitList);
        if (newFLG > 15):
            newFLG = 0;
        newFLG = newFLG + 1;
        tempFLGbitList = Byte(self._flgbyte).bitList(newFLG, 8);
        for idx in range(4, 8):
           self.__flgbyteList[idx] = tempFLGbitList[idx];
        newFLG = Byte(self._flgbyte).integer(self.__flgbyteList);
        return newFLG;


    #Testing Code
if(__name__ == '__main__'):
    newFLG = Frame(4).setFrameType(1);
    print newFLG;
    responseFlag = Frame(newFLG).checkFrameType()
    print responseFlag;
    newFLG = Frame(3).increaseFrameFlag();
    print newFLG;
    newFLG = Frame(16).FlagSequNum();
    print newFLG;