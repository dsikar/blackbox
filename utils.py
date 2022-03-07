import subprocess
import shlex
import readID as readIDVar
from logging import writelog, checkLogDir
import datetime
import time
import config
import constants



def DecodePacketType( packet_id ) :

  PacketTypeText = str( packet_id ) + "ABC";
  
  if ( packet_id == constants.PACKET_ID_POINT_INFO_REQUEST ) : 
    PacketTypeText = "PACKET_ID_POINT_INFO_REQUEST"
  elif ( packet_id == constants.PACKET_ID_POINT_INFO_REPLY ) : 
    PacketTypeText = "PACKET_ID_POINT_INFO_REPLY"
  elif ( packet_id == constants.PACKET_ID_PANEL_INFORMATION ) : 
    PacketTypeText = "PACKET_ID_PANEL_INFORMATION"      
  elif ( packet_id == constants.PACKET_ID_PANEL_INFORMATION_REQ ) : 
    PacketTypeText = "PACKET_ID_PANEL_INFORMATION_REQ"   
  else :
    PacketTypeText = "--"
  
  return PacketTypeText
  

def DecodeDeviceType( device_type_id ) :

  DeviceTypeText = "Unknown"
  
  if ( device_type_id == constants.DEVICE_ID_855_PH ) : 
    DeviceTypeText = "855PH"
  elif ( device_type_id == constants.DEVICE_ID_855_P ) : 
    DeviceTypeText = "855P"
  elif ( device_type_id == constants.DEVICE_ID_855_H ) : 
    DeviceTypeText = "855H"      
  elif ( device_type_id == constants.DEVICE_ID_855_PC ) : 
    DeviceTypeText = "855PC"   
  elif ( device_type_id == constants.DEVICE_ID_850_H ) : 
    DeviceTypeText = "850H"   
  elif ( device_type_id == 253 ) : 
    DeviceTypeText = "Empty" 
  else :
    DeviceTypeText = "--"
  
  return DeviceTypeText


def DecodeChannelType( channel_type_value ) : 

  ChannelTypeText = "Unknown"
  
  if ( channel_type_value == constants.CHANNEL_TYPE_INVALID ) : 
    ChannelTypeText = "N/A"
  elif ( channel_type_value == constants.CHANNEL_TYPE_DEGREES_C ) : 
    ChannelTypeText = "oC"
  elif ( channel_type_value == constants.CHANNEL_TYPE_DEGREES_F ) : 
    ChannelTypeText = "oF"      
  elif ( channel_type_value == constants.CHANNEL_TYPE_PPM ) : 
    ChannelTypeText = "ppm"   
  elif ( channel_type_value == constants.CHANNEL_TYPE_PERCENT_FOOT ) : 
    ChannelTypeText = "%ft"   
  elif ( channel_type_value == constants.CHANNEL_TYPE_PERCENT_METER ) : 
    ChannelTypeText = "%m"   
  elif ( channel_type_value == constants.CHANNEL_TYPE_Y_VALUE ) : 
    ChannelTypeText = "Y Value"   
  elif ( channel_type_value == constants.CHANNEL_TYPE_AMPS ) : 
    ChannelTypeText = "Amps"   
  elif ( channel_type_value == constants.CHANNEL_TYPE_VOLTS ) : 
    ChannelTypeText = "Volts"   
  elif ( channel_type_value == constants.CHANNEL_TYPE_NOT_INSTALLED ) : 
    ChannelTypeText = "Not Installed"       
  elif ( channel_type_value == constants.CHANNEL_TYPE_MILLI_AMP ) : 
    ChannelTypeText = "mA"   
  else :
    ChannelTypeText = "--"
    
  return ChannelTypeText
  
  
def DeviceAttribsAtString( device_attribs ) : 

  DeviceAttribstext = ""

  # bit 0 supports input
  # bit 1 supports output
  # bit 2 solo
  # bit 3 base of split
  # bit 4 part of split
  # bit 5 - unused
  # bit 6 sounder
  # bit 7 isolation allowed

  return  DeviceAttribsAtString; 
  
def DecodeAnalogueValueToHuman( unit_type, converted_reading ) : 

  RealWorldReading = "??"
  
  if ( unit_type == constants.CHANNEL_TYPE_INVALID ) : 
    RealWorldReading = "--"
  elif ( unit_type == constants.CHANNEL_TYPE_DEGREES_C ) : 
    RealWorldReading = str( converted_reading - 50 ) + DecodeChannelType( unit_type ) 
  elif ( unit_type == constants.CHANNEL_TYPE_DEGREES_F ) : 
    RealWorldReading = str( converted_reading ) + DecodeChannelType( unit_type ) 
  elif ( unit_type == constants.CHANNEL_TYPE_PPM ) : 
    RealWorldReading = str( converted_reading ) + DecodeChannelType( unit_type )     
  elif ( unit_type == constants.CHANNEL_TYPE_PERCENT_FOOT ) : 
    RealWorldReading = str( converted_reading / 10 ) + DecodeChannelType( unit_type )  
  elif ( unit_type == constants.CHANNEL_TYPE_PERCENT_METER ) : 
    RealWorldReading = str( converted_reading / 10 ) + DecodeChannelType( unit_type )     
  elif ( unit_type == constants.CHANNEL_TYPE_Y_VALUE ) : 
    RealWorldReading = str( converted_reading / 100 ) + DecodeChannelType( unit_type )   
  elif ( unit_type == constants.CHANNEL_TYPE_AMPS ) : 
    RealWorldReading = str( ( converted_reading - 100 ) / 5 ) + DecodeChannelType( unit_type ) 
  elif ( unit_type == constants.CHANNEL_TYPE_VOLTS ) : 
    RealWorldReading = str( converted_reading / 5 ) + DecodeChannelType( unit_type )    
  elif ( unit_type == constants.CHANNEL_TYPE_NOT_INSTALLED ) : 
    RealWorldReading = "- -"       
  elif ( unit_type == constants.CHANNEL_TYPE_MILLI_AMP ) : 
    RealWorldReading = str( converted_reading / 5 ) + DecodeChannelType( unit_type ) 
  else :
    RealWorldReading = "--"
  
  return RealWorldReading;
  
  
def DecodeAlarmState( InstantAlarmState ) :

  InstantAlarmStateText = ""
  
  if ( InstantAlarmState == constants.POINT_REPLY_INSTANT_ALARM_STATE_CLEAR ) : 
    InstantAlarmStateText = "Clear"
  elif ( InstantAlarmState == constants.POINT_REPLY_INSTANT_ALARM_STATE_PRE_ALARM ) : 
    InstantAlarmStateText = "Pre-Alarm"
  elif ( InstantAlarmState == constants.POINT_REPLY_INSTANT_ALARM_STATE_VERIFYING ) : 
    InstantAlarmStateText = "Verifying"      
  elif ( InstantAlarmState == constants.POINT_REPLY_INSTANT_ALARM_STATE_ACTIVE ) :
    InstantAlarmStateText = "Active"      
  elif ( InstantAlarmState == constants.POINT_REPLY_INSTANT_ALARM_STATE_RESETTING ) :
    InstantAlarmStateText = "Resetting"      
  elif ( InstantAlarmState == constants.POINT_REPLY_INSTANT_ALARM_STATE_TEST ) :
    InstantAlarmStateText = "Resetting"  
  elif ( InstantAlarmState == constants.POINT_REPLY_INSTANT_ALARM_STATE_WARNING ) :
    InstantAlarmStateText = "Warning"  
  else :
    InstantAlarmStateText = "--"    
  
  return InstantAlarmStateText;


## END OF FILE 