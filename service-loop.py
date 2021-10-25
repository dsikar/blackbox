import subprocess
import shlex
import readID as readIDVar
from logging import writelog, checkLogDir
import datetime
import time
import config
import constants


poll_list = [ True, True ]

point_poll_sucess = True;

ptp_sequence = 6

use_mxspeak_6 = True;


def hex_to_int( value ) :

  return int( value, 16 )


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
  

def decode_point_info_reply( packet_to_decode ) : 

    global point_poll_sucess
    global use_mxspeak_6;
    
    point_poll_sucess = True

    length = len( packet_to_decode )

    # remove checksum from end
    shorter = packet_to_decode[:length - 3]

    varlist = map(hex_to_int, shorter .split(','));
    
    # remove SOH and sequence number
    varlist.pop(0)
    varlist.pop(0)
    
    offset = 0
    if ( use_mxspeak_6 == False) :
       offset = -1
    

    point_number = varlist[ constants.POINT_REPLY_POINT_ADDRESS_OFFSET + offset ]
    loop_number  = varlist[ constants.POINT_REPLY_CHANNEL_ADDRR_OFFSET + offset ]
    
    print( "\nPoint Information Reply Packet :   Loop " + str(loop_number)  + " Point " + str(point_number) )
    
    print( "state       " + str(  varlist[ constants.POINT_REPLY_HIGH_LEVEL_STATUS_OFFSET + offset ] ) + "     Zero = success")
     
    if ( varlist[ constants.POINT_REPLY_HIGH_LEVEL_STATUS_OFFSET + offset ] == 0 ) :
    
       # header
       point_number = varlist[ constants.POINT_REPLY_POINT_ADDRESS_OFFSET + offset ]
       loop_number  = varlist[ constants.POINT_REPLY_CHANNEL_ADDRR_OFFSET + offset ]    
       print( "\nPoint Information Reply Packet :   Loop " + str(loop_number)  + " Point " + str(point_number) )
       
       print ( "Flags       " + str( varlist[ constants.POINT_REPLY_FLAGS_OFFSET + offset] ) )
       print ( "Node        " + str( varlist[ constants.POINT_REPLY_NODE_OFFSET  + offset] ) )
       print ( "Channel     " + str( varlist[ constants.POINT_REPLY_CHANNEL_OFFSET + offset] ) )
       print ( "Chan addr   " + str( varlist[ constants.POINT_REPLY_CHANNEL_ADDRR_OFFSET  + offset] ) + "    this is the loop number" )
       print ( "Pnt cat     " + str( varlist[ constants.POINT_REPLY_POINT_CATEGORY_OFFSET + offset] ) )
       print ( "Pnt addr    " + str( varlist[ constants.POINT_REPLY_POINT_ADDRESS_OFFSET  + offset]  ) )
       print ( "log part1   " + str( varlist[ constants.POINT_REPLY_LOG_ADDR_PART_1_OFFSET + offset] ) )
       print ( "log part2   " + str( varlist[ constants.POINT_REPLY_LOG_ADDR_PART_2_OFFSET + offset] ) )
       
       DeviceTypeAsString = DecodeDeviceType( varlist[ constants.POINT_REPLY_DEVICE_TYPE_OFFSET + offset ] )
       print ( "Device type " + str( varlist[ constants.POINT_REPLY_DEVICE_TYPE_OFFSET + offset ] ) + "    " + DeviceTypeAsString )
       
       # TODO Mike Mayhew - we need to define DecodeDeviceAttibs
       # DeviceAttribsAtString = DecodeDeviceAttibs( varlist[ constants.POINT_REPLY_ATTRIBS_OFFSET ] )
       print ( "Attribs     " + str( varlist[ constants.POINT_REPLY_ATTRIBS_OFFSET + offset ] ) )
       print ( "group pt1   " + str( varlist[ constants.POINT_REPLY_GROUP_PT1_OFFSET + offset ] ) )
       print ( "group pt2   " + str( varlist[ constants.POINT_REPLY_GROUP_PT2_OFFSET + offset ] ) )
       print ( "Area type   " + str( varlist[ constants.POINT_REPLY_AREA_TYPE_OFFSET + offset ] ) )
       print ( "Area nmbr   " + str( varlist[ constants.POINT_REPLY_AREA_NUMNER + offset ] ) )
       print ( "Sector      " + str( varlist[ constants.POINT_REPLY_SECTOR     + offset] ) + "    254 if not sector")
       print ( "Loop type   " + str( varlist[ constants.POINT_REPLY_LOOP_TYPE  + offset] ) + "      1 is MX")
       print ( "raw dev id  " + str( varlist[ constants.POINT_REPLY_RAW_DEV_ID + offset] ) )


       print ( "Raw 1       " + str( varlist[ constants.POINT_REPLY_RAW_ANALOGUE_1 + offset ] ) )
       print ( "Raw 2       " + str( varlist[ constants.POINT_REPLY_RAW_ANALOGUE_2 + offset ] ) )
       print ( "Raw 3       " + str( varlist[ constants.POINT_REPLY_RAW_ANALOGUE_3 + offset ] ) )
              
       print ( "LTA flag    " + str( varlist[ constants.POINT_REPLY_LTA_FLAGS + offset ] ) )
       print ( "Raw LTA     " + str( varlist[ constants.POINT_REPLY_RAW_LTA   + offset ] ) )
       print ( "Dirty       " + str( varlist[ constants.POINT_REPLY_DIRTINESS + offset ] ) )       
       
       
       ChannelTypeAsString = DecodeChannelType( varlist[ constants.POINT_REPLY_UNIT_OF_MEASURE_1 + offset ] )
       print ( "units  1    " + str( varlist[ constants.POINT_REPLY_UNIT_OF_MEASURE_1 + offset] ) + "  " + ChannelTypeAsString)
       ChannelTypeAsString = DecodeChannelType( varlist[ constants.POINT_REPLY_UNIT_OF_MEASURE_2 + offset ] )
       print ( "units  2    " + str( varlist[ constants.POINT_REPLY_UNIT_OF_MEASURE_2 + offset] ) + "  " + ChannelTypeAsString )
       ChannelTypeAsString = DecodeChannelType( varlist[ constants.POINT_REPLY_UNIT_OF_MEASURE_3 + offset ] )
       print ( "units  3    " + str( varlist[ constants.POINT_REPLY_UNIT_OF_MEASURE_3 + offset] ) + "  " + ChannelTypeAsString)
       
       DisplayReadingAsString = DecodeAnalogueValueToHuman( varlist[ constants.POINT_REPLY_UNIT_OF_MEASURE_1 + offset], varlist[ constants.POINT_REPLY_CONVERTED_VALUE_1 + offset ] )
       print ( "Conv 1      " + str( varlist[ constants.POINT_REPLY_CONVERTED_VALUE_1 + offset ] ) + "  " + DisplayReadingAsString )
       DisplayReadingAsString = DecodeAnalogueValueToHuman( varlist[ constants.POINT_REPLY_UNIT_OF_MEASURE_2 + offset], varlist[ constants.POINT_REPLY_CONVERTED_VALUE_2 + offset ] )
       print ( "Conv 2      " + str( varlist[ constants.POINT_REPLY_CONVERTED_VALUE_2 + offset ] ) + "  " + DisplayReadingAsString)
       DisplayReadingAsString = DecodeAnalogueValueToHuman( varlist[ constants.POINT_REPLY_UNIT_OF_MEASURE_3 + offset], varlist[ constants.POINT_REPLY_CONVERTED_VALUE_3 + offset ] )
       print ( "Conv 3      " + str( varlist[ constants.POINT_REPLY_CONVERTED_VALUE_3 + offset ] ) + "  " + DisplayReadingAsString )
       
       InstantAlarmStateAsString = DecodeAlarmState( varlist[ constants.POINT_REPLY_INSTANT_ACTIVE + offset] )
       print ( "now Alarm   " + str( varlist[ constants.POINT_REPLY_INSTANT_ACTIVE + offset ] ) + "   " + InstantAlarmStateAsString )
       print ( "now Fault   " + str( varlist[ constants.POINT_REPLY_INSTANT_FAULT + offset ] ) )
       
       ConfirmedAlarmStateAsString = DecodeAlarmState( varlist[ constants.POINT_REPLY_CONFIRMED_ACTIVE + offset] )
       print ( "Confirm Alm " + str( varlist[ constants.POINT_REPLY_CONFIRMED_ACTIVE + offset ] ) + "   " + ConfirmedAlarmStateAsString )
       print ( "Confirm Flt " + str( varlist[ constants.POINT_REPLY_CONFIRMED_FAULT + offset ] ) )
       
       AckedAlarmStateAsString = DecodeAlarmState( varlist[ constants.POINT_REPLY_ACKED_ACTIVE + offset] )
       print ( "Acked Alm   " + str( varlist[ constants.POINT_REPLY_ACKED_ACTIVE + offset ] ) + "   " + AckedAlarmStateAsString )
       print ( "Acked Flt   " + str( varlist[ constants.POINT_REPLY_ACKED_FAULT + offset ] ) )
       
       print ( "OP Is Forced" + str( varlist[ constants.POINT_REPLY_IS_OUTPUT_FORCED + offset ] ) )
       print ( "OP Unforced " + str( varlist[ constants.POINT_REPLY_OUTPUT_UNFORCED_STATE + offset ] ) )
       print ( "OP Forced   " + str( varlist[ constants.POINT_REPLY_OUTPUT_FORCED_STATE + offset ] ) )

        
       print ( "----" )
       
       # WE ARE ONLY LOGGING GOOD REPLIES
       # Replies where there is a device.

       packet_to_log = ""
        
       for el in varlist:
          packet_to_log += str(el) + ","
          
       packet_to_log += "\n"  
          
       writelog(packet_to_log,logfile)      
       
       #print("LOG THIS [new]: \n" + packet_to_log )
       
    else:
       point_poll_sucess = False

    
def decode_panel_info_reply( packet_to_decode ) :     
    
    global point_poll_sucess
    global use_mxspeak_6;
    
    point_poll_sucess = True

    length = len( packet_to_decode )

    # remove checksum from end
    shorter = packet_to_decode[:length - 3]

    varlist = map(hex_to_int, shorter .split(','));
    
    # remove SOH and sequence number
    varlist.pop(0)
    varlist.pop(0)

    print( "\nPanel Information" )
       
    
    # get rid of the header

    varlist.pop(0)
    varlist.pop(0)
    varlist.pop(0)
    varlist.pop(0)
    varlist.pop(0)
    varlist.pop(0)
    varlist.pop(0)
    varlist.pop(0)
    varlist.pop(0)
    
    # MXSpeak 6 header is 4 bytes longer
    if ( use_mxspeak_6 ) :
        varlist.pop(0)
        varlist.pop(0)
        varlist.pop(0)
        varlist.pop(0)
    
      
    print( "Time Date (secs): " + str(varlist[0]) + " " + str(varlist[1]) + " " + str(varlist[2]) + " " + str( varlist[3]) )
    print( "panel Version   : " + str(varlist[4]) + " " + str(varlist[5]) + " " + str(varlist[6]))
    print( "Days Left Auto  : " + str(varlist[7]) + " "+  str(varlist[8]) )
    print( "Market Channel  : " + str(varlist[9]) )
    print( "Flags           : " + str(varlist[10]) + " " + str(varlist[11]))
    print( "equipment       : " + str(varlist[12]) + " " + str(varlist[13]))
    print( "compat          : " + str(varlist[14]) + " " + str(varlist[15]))
    print( "MXSpeak         : " + str(varlist[16]) + "    - 0 MXspeak 5, 1 MXSpeak 6 " )
    
    if ( varlist[16] == 1 ) :
        # print( "Set to MXspeak 6")
        use_mxspeak_6 = True;
    

    print ( "\n" )       
    


def decode_reply_packet( packet_to_decode ) :

    global use_mxspeak_6;

    length = len( packet_to_decode )

    shorter = packet_to_decode[:length - 3]

    varlist = map(hex_to_int, shorter .split(','));


    # remove PTP header info
    varlist.pop(0)
    varlist.pop(0)

    print_me = "PACKET TO DECODE : "
    for el in varlist:
       print_me += "," + str(el);
    
    print( print_me )
    
    PacketID = 0;
    
    #print ( "Length  : " + str( varlist [ 0 ] ))
    #print ( "MXSpeak 6 indicator  : " + str( varlist [ 1 ] ) + " - 228 indicates MXSpeak 6")
    if ( varlist [ 1 ] == 228 ) : 
        use_mxspeak_6 = True;
        #print( "SET MXSPEAK 6");
        PacketID = varlist[ constants.OFFSET_FOR_PACKET_TYPE_MXSPEAK_6 ];
        #print ( "Reply  MX6 : " + str( PacketID ) + "  " + DecodePacketType(PacketID))
    else : 
        use_mxspeak_6 = False;
        #print( "SET MXSPEAK 5");
        PacketID = varlist[ constants.OFFSET_FOR_PACKET_TYPE_MXSPEAK_5 ];
        #print ( "Reply  MX5 : " + str( PacketID ) + "  " + DecodePacketType(PacketID))

   
    # --------------------


    if ( PacketID == constants.PACKET_ID_POINT_INFO_REPLY ) : 
      decode_point_info_reply( packet_to_decode ) 
      
    
    if ( PacketID == constants.PACKET_ID_PANEL_INFORMATION ) : 
      decode_panel_info_reply( packet_to_decode ) 
      
    else :
      print ( "Reply Packet Type " + str( varlist[ constants.OFFSET_FOR_PACKET_TYPE_MXSPEAK_6 ] ) )


def FormRequestPacket( loop, point  ) :

    # without PTP framing
    # without checksum
    #
    # L - length
    # SIG - MXSpeak 6 signature, (228) only if MXSpeak 6
    # packet stuff starts at 12
    #
    # PACKET_ID_POINT_INFO_REQUEST = 148 - hex95
    #
    # MXSPEAK 6
    # 228 - mxspeak 6 indicator
    # 0   - network node
    # 0   - channel
    # 0   - destination channel address
    # 4   - deatination task
    # 253 - source channel address 
    # 146 - source task
    # 0   - marker
    # 148 - packet type - point info requred.
    # 0   - reserved -  zero
    #
    
    
    # MXSPEAK 5
    # 0   - DN destination node
    # 0   - channel
    # 0   - destination channel address
    # 1   - destination task
    # 0   - source channel address 
    # 0   - source task
    # 0   - marker
    # 148 - packet type - point info requred.

    
    #                        9,     0,  0 ,0,  1   ,0,  0,  123,26
    
    #
    #                        L  SIG DN SN DCH  DT SCH  STSK MK PKT RS \/ packet is here
    SamplePacket_mxspeak6 = "58,228,0, 0, 0,  4,  253, 146, 0, 148,0, 12,1,0,1,0,254,0,0,1,3,0,0,3,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,0,10"
    SamplePacket_mxspeak5 = "57    ,0, 0, 0,  1,    0,   0, 0, 148,   0 , 0 ,1,0,1,0,254,0,0,1,3,0,0,3,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,0,10"


    global ptp_sequence
    global use_mxspeak_6

    if ( use_mxspeak_6 ) : 
        varlist = map(int, SamplePacket_mxspeak6 .split(','));
        #print( "USING MXSPEAK 6")
    else : 
        varlist = map(int, SamplePacket_mxspeak5 .split(','));
        #print( "USING MXSPEAK 5")

    detail_display = 0
    
    # to be on the safe side
    # check the packet type.
    
    if ( use_mxspeak_6 ) : 
        if ( varlist[ constants.OFFSET_FOR_PACKET_TYPE_MXSPEAK_6 ] == constants.PACKET_ID_POINT_INFO_REQUEST ) : 
            varlist[ constants.POINT_INFO_REQUEST_POINT_OFFSET ] = point
            varlist[ constants.POINT_INFO_REQUEST_LOOP_OFFSET  ] = loop
            
            if ( config.DISPLAY_POINT_REQUEST_PACKETS_OVERVIEW == 1 ) :
                print( "\nRequest -  Loop : " + str( loop ) + ",  Point : " + str( point ) )            

                if ( config.DISPLAY_POINT_REQUEST_PACKETS_DETAIL == 1 ) :
                   print ( "Point Information Request : Node      " + str(  varlist[ constants.POINT_INFO_REQUEST_NODE_OFFSET ] ) )
                   print ( "Point Information Request : channel   " + str(  varlist[ constants.POINT_INFO_REQUEST_CHANNEL_OFFSET ] )  + "   MXSpeak 6 12 is main processor")
                   print ( "Point Information Request : chan addr " + str(  varlist[ constants.POINT_INFO_REQUEST_LOOP_OFFSET ] )  + "   Channel 12, channel addr 1 = loop A")
                   print ( "Point Information Request : pnt cat   " + str(  varlist[ constants.POINT_INFO_REQUEST_POINT_CATEGORY_OFFSET ] )  + "   0 - real points")
                   print ( "Point Information Request : pnt addr  " + str(  varlist[ constants.POINT_INFO_REQUEST_POINT_OFFSET ] ) )
                   print ( "Point Information Request : log pt 1  " + str(  varlist[ constants.POINT_INFO_REQUEST_LOGICAL_ADDR_PT1_OFFSET ] ) )
                   print ( "Point Information Request : log pt 2  " + str(  varlist[ constants.POINT_INFO_REQUEST_LOGICAL_ADDR_PT2_OFFSET ] ) )
                   print ( "Point Information Request : dev cat   " + str(  varlist[ constants.POINT_INFO_REQUEST_DEVICE_CATEGORY_OFFSET ] ) )

                else: 
                   # If here something went wrong.  This function is only for point info request packets.
                   print ( "xx Packet Type " + str(  varlist[ constants.OFFSET_FOR_PACKET_TYPE_MXSPEAK_6 ] ) )

    else :
        # MXSPEAK 5
        #
        #
        if ( varlist[ constants.OFFSET_FOR_PACKET_TYPE_MXSPEAK_5 ] == constants.PACKET_ID_POINT_INFO_REQUEST ) : 

            varlist[ constants.POINT_INFO_REQUEST_POINT_OFFSET_MXSPEAK_5 ] = point
            varlist[ constants.POINT_INFO_REQUEST_LOOP_OFFSET_MXSPEAK_5  ] = loop


    # Start with SOH and low level sequence number.
    result = "1" # + str ( ptp_sequence )

    # Add the PTP sequence number to the packet.
    varlist.insert(0, ptp_sequence)

    ptp_sequence += 1
    if ptp_sequence > 8 : 
     ptp_sequence = 5
    
    checksum = 0
    for el in varlist:

      checksum += el
      result += "," + str(el);

    checksum = checksum % 256

    varlist.append( checksum )

    #print( "Calculated checksum: " + str(checksum))

    result += "," + str(checksum)

    #print( "Constructed Packet to send : \n" + result )

    return result 


def PointInformationScan(   ) :

    # initial dealy between polls while we work out what is there.
    delaybetweenpolls = 0.5


    # 'poll_list' is a store indicating whether we should poll this device, start at TRUE.
    # One store for all loop.  points in loop 1, then loop 2....
    # Indexed by point number, we set '0' as False, this is unused.

    poll_list = [ False ]
    for loop in range( constants.MAX_LOOP_TO_SCAN ) :
        for x in range( constants.MAX_ADDRESSES_PER_LOOP ):
          poll_list.append( True )

    # Declare loop variables, with start values
    point_address = 1
    current_loop  = 1


    while(True):

        startTime = datetime.datetime.now();

        poll_list_index = ((current_loop - 1) * constants.MAX_ADDRESSES_PER_LOOP) + point_address
        
        if ( poll_list[ poll_list_index ] == True ) : 

            #print "Packet in jobs list : \n"+content
            
            # TO DO
            # Not ideal, but adjust the packet for the loop and point address
            packettosend = FormRequestPacket( current_loop, point_address )
            print( "Sending Request for  - Loop " + str( current_loop ) + " Pnt " + str( point_address ) )
            
            #print(  packettosend  )

            action = "python packetizer/pointinfotest.py " + packettosend 
            #print(action)
            payload = subprocess.check_output(shlex.split(action));
            if len(payload) > 1: #for some reason printing an empty payload still constitutes to greater than 0, so we use 1 instead
                # writelog(payload,logfile)
                # TODO adjust to windows 7/10
                print("Reply from Panel, Length " + str( len( payload ) ) )
                #print(payload)
                if (len(payload) > 10) :
                  decode_reply_packet(payload) 
                  if( point_poll_sucess == False) :
                    poll_list[ poll_list_index ] = False
                #print "Payload response to serviced packet : \n"+payload; 
            else:
                #print("this is the payload" + str(payload))
                print "No device recorded for this point"

            time.sleep(delaybetweenpolls) 

        point_address += 1
        
        # If we have got to the end of a loop.
        # start again at the start of the next loop.
        if (point_address >constants.MAX_ADDRESSES_PER_LOOP):         
            point_address = 1

            current_loop += 1
            if (current_loop > constants.MAX_LOOP_TO_SCAN): 
                current_loop = 1

                x = poll_list.count( True )
                print( "Number of devices replying to poll " + str( x ) ) 
                # if very few devices, we need to chill the poll time,
                if (( x * delaybetweenpolls ) < ( min_time_between_polls )) :
                    delaybetweenpolls = min_time_between_polls / x
                    print( "Updated poll time : " + str( delaybetweenpolls ) )
                   

def FormOpeningRequestPacket(   ) :

    print( "Form request packet type 26" )

    # Packet type is 26
    # Destination configuration manager = ID 3

    # without PTP framing
    # without checksum
    #
    
    # length
    # destination node             = 0 local
    # channel                      = 0
    # destination channel address  = 0
    # destination task             - 1 local
    # source channel               = 0
    # source task                  = 0
    # marker                       = any thing - 123
    # packet ID                    = 26

    
    #SamplePacket = "16,228,0,0,0,4,253,26,0,12,1,0,1,0,254,0"
    
    #               L D C A D T S  M   PK
    SamplePacket = "9,0,0,0,1,0,0,123,26"

 
    global ptp_sequence

    varlist = map(int, SamplePacket .split(','));

    length = len( varlist )
    
    result = "error"

  
    # Start with SOH and low level sequence number.
    result = "1" # + str ( ptp_sequence )

    # Add the PTP sequence number to the packet.
    varlist.insert(0, ptp_sequence)

    ptp_sequence += 1
    if ptp_sequence > 8 : 
     ptp_sequence = 5
    
    checksum = 0
    for el in varlist:
      checksum += el
      result += "," + str(el);

    checksum = checksum % 256

    varlist.append( checksum )

    result += "," + str(checksum)

    print( "Constructed Packet to send : \n" + result )

    return result 

def OpeningPacketsMode( ) :

    print( "\nRequest panel info\n")
    PanelInfoRequest =  FormOpeningRequestPacket(  ) 
  

    action = "python packetizer/pointinfotest.py " + PanelInfoRequest 


    payload = subprocess.check_output(shlex.split(action));
    if len(payload) > 1: #for some reason printing an empty payload still constitutes to greater than 0, so we use 1 instead
        # writelog(payload,logfile)
        # TODO adjust to windows 7/10

        print(payload)
        
        if (len(payload) > 10) :
          print( "HERE" )
          decode_reply_packet(payload) 
        #  if( point_poll_sucess == False) :
        #    poll_list[ poll_list_index ] = False

    else:
        #print("this is the payload" + str(payload))
        print "No device recorded for this point",
  
  
    if len(payload) == 2:
  
        PanelInfoRequest =  FormOpeningRequestPacket(  ) 

        action = "python packetizer/pointinfotest.py " + PanelInfoRequest 

        payload = subprocess.check_output(shlex.split(action));
        if len(payload) > 1: #for some reason printing an empty payload still constitutes to greater than 0, so we use 1 instead

            #print(payload)
            
            if (len(payload) > 10) :
              decode_reply_packet(payload)
         
              
            #  if( point_poll_sucess == False) :
            #    poll_list[ poll_list_index ] = False
            
            print "Payload response to serviced packet : \n"+payload; 
        else:
            #print("this is the payload" + str(payload))
            print "No device recorded for this point",


#
# START OF MAIN
#



delaybetweenpolls = 0.2
min_time_between_polls = 5


pid = readIDVar.readID();
pid = pid.strip()
entry = "Logging Panel Points Panel ID: " + str(pid) + '\n\n'
print(entry)


# check logging directory
checkLogDir() 

logfile = str(datetime.datetime.today().strftime('%Y%m%d%H%M%S'))
logfile += '_BlackBox.log'

OpeningPacketsMode()

print(entry)
writelog(entry, logfile)
 
PointInformationScan()



          
   


          

+ '\n\n'
print(entry)


# check logging directory
checkLogDir() 

logfile = str(datetime.datetime.today().strftime('%Y%m%d%H%M%S'))
logfile += '_BlackBox.log'

OpeningPacketsMode()

print(entry)
writelog(entry, logfile)
 
PointInformationScan()


               


          
     


          
file)
 
PointInformationScan()


               


          
