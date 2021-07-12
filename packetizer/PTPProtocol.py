'''
* @brief
* The class is provided for writing and reading in PTP protocol with PacketReader.py

* Input: dataTransfer, frame
* Output: received packet
'''

from PacketReader import PacketReader;
from PacketWriter import PacketWriter;

# the imports below are used for testing
from serialdatatransfer import SerialDataTransfer;
from header import LocalHeader;
import packetids as packetID;
from content import Content;
from packet import Packet;
from pointinformationcontent import *;

class PTPProtocol:

    def __init__(self, dataTransfer):
        self._dataTransfer = dataTransfer;
        self._PacketReaderObj = PacketReader(self._dataTransfer);
        self._PacketWriterObj = PacketWriter(self._dataTransfer);

    def Write(self, packet, flagbyte):
        self._PacketWriterObj.Write(packet, flagbyte);

    def Read(self):
        packet = None;
        flag = self._PacketWriterObj.returnFlag();
        packet = self._PacketReaderObj.Read(flag);
        return packet;


if(__name__ == '__main__'):
    dataTransfer = SerialDataTransfer('COM1');
    var = PTPProtocol(dataTransfer);

    header = LocalHeader(packetID.spkd_ID_POINT_INFO_REQUEST);
    header.setParameter("destinationTask", 0x04);
    header.setParameter("sourceChannelAddress", 0xFD); #values sent by consys for header replicated here
    header.setParameter("sourceTask",0x92);

    header.IgnoreReserved(True);

    content  =  PointInformationContent();
    packet   =  Packet(header, content);
    FLG = 0x01;
    # if flag is needed to be changed, change it here

    var.Write(packet, FLG);
    var.Read();