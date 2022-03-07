import subprocess
import shlex
import readID as readIDVar
from logging import writelog, checkLogDir
import datetime
import time
import config
import constants
import utils


point_poll_sucess = True;

ptp_sequence = constants.MIN_PTP_SEQUENCE

use_mxspeak_6 = True;

current_node = constants.MIN_NETWORK_NODE

glb_reply_indicates_loop_not_there = False
glb_reply_indicates_no_more_points_on_loop = False


glb_point_info_client_number = 0


def hex_to_int( value ) :

  return int( value, 16 )
  

def decode_point_info_reply( packet_to_decode ) : 

    global point_poll_sucess
    global use_mxspeak_6;
    global glb_reply_indicates_loop_not_there 
    global glb_point_info_client_number
    global glb_reply_indicates_no_more_points_on_loop
    
    glb_reply_indicates_loop_not_there = False
    point_poll_sucess = True


    length = len( packet_to_decode )

    # remove checksum from end
    shorter = packet_to_decode[:length - 3]

    varlist = map(hex_to_int, shorter .split(','));
    
    # remove SOH and sequence number
    varlist.pop(0)
    varlist.pop(0)
    
    offset = 0
    node_number  = varlist[ constants.POINT_REPLY_NODE_OFFSET_MXSPEAK_6 ];
    if ( use_mxspeak_6 == False) :
       offset = -1
       node_number  = varlist[ constants.POINT_REPLY_NODE_OFFSET_MXSPEAK_5 ];
    
 
    point_number = varlist[ constants.POINT_REPLY_POINT_ADDRESS_OFFSET + offset ]
    loop_number  = varlist[ constants.POINT_REPLY_CHANNEL_ADDRR_OFFSET + offset ]
    
    # zero is success 
    state = varlist[ constants.POINT_REPLY_HIGH_LEVEL_STATUS_OFFSET + offset ]
    
    if ( state == 0 ) : 
    
      glb_point_info_client_number = ( varlist[ constants.POINT_REPLY_CLIENT_KEY_1 + offset ] * 256 ) + varlist[ constants.POINT_REPLY_CLIENT_KEY_2 + offset ]
      print( "\nClient code : " + str( glb_point_info_client_number ))
    
      print( "\nPoint Information Reply Packet : Node " + str(node_number) + " Loop " + str(loop_number)  + " Point " + str(point_number) )
      
      glb_reply_indicates_no_more_points_on_loop = False
    else : 
      fault_state =  varlist[ constants.POINT_REPLY_FLAGS_OFFSET + offset] 
      print( "\nPoint Information Reply Packet : Request invalid (point not in config)  (Flags " + str( fault_state ) + ")" )
      
      glb_reply_indicates_no_more_points_on_loop = True
      print( "Scan Complete - move to next loop" )

      
    if ( state == 0 ):
    
       # header
       point_number = varlist[ constants.POINT_REPLY_POINT_ADDRESS_OFFSET + offset ]
       loop_number  = varlist[ constants.POINT_REPLY_CHANNEL_ADDRR_OFFSET + offset ]    
       #print( "\nPoint Information Reply Packet :   Node " + str(node_number) + " Loop " + str(loop_number)  + " Point " + str(point_number) )
       
        
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


    Display = True
    if (( state == 0 ) & ( Display == True)):
    
       # header
       point_number = varlist[ constants.POINT_REPLY_POINT_ADDRESS_OFFSET + offset ]
       loop_number  = varlist[ constants.POINT_REPLY_CHANNEL_ADDRR_OFFSET + offset ]    
       #print( "\nPoint Information Reply Packet :   Node " + str(node_number) + " Loop " + str(loop_number)  + " Point " + str(point_number) )
       
       print ( "Flags       " + str( varlist[ constants.POINT_REPLY_FLAGS_OFFSET + offset] ) )
       print ( "Node        " + str( varlist[ constants.POINT_REPLY_NODE_OFFSET  + offset] ) )
       print ( "Channel     " + str( varlist[ constants.POINT_REPLY_CHANNEL_OFFSET + offset] ) )
       print ( "Chan addr   " + str( varlist[ constants.POINT_REPLY_CHANNEL_ADDRR_OFFSET  + offset] ) + "    this is the loop number" )
       print ( "Pnt cat     " + str( varlist[ constants.POINT_REPLY_POINT_CATEGORY_OFFSET + offset] ) )
       print ( "Pnt addr    " + str( varlist[ constants.POINT_REPLY_POINT_ADDRESS_OFFSET  + offset]  ) )
       print ( "log part1   " + str( varlist[ constants.POINT_REPLY_LOG_ADDR_PART_1_OFFSET + offset] ) )
       print ( "log part2   " + str( varlist[ constants.POINT_REPLY_LOG_ADDR_PART_2_OFFSET + offset] ) )
       
       DeviceTypeAsString = utils.DecodeDeviceType( varlist[ constants.POINT_REPLY_DEVICE_TYPE_OFFSET + offset ] )
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
       
       
       ChannelTypeAsString = utils.DecodeChannelType( varlist[ constants.POINT_REPLY_UNIT_OF_MEASURE_1 + offset ] )
       print ( "units  1    " + str( varlist[ constants.POINT_REPLY_UNIT_OF_MEASURE_1 + offset] ) + "  " + ChannelTypeAsString)
       ChannelTypeAsString = utils.DecodeChannelType( varlist[ constants.POINT_REPLY_UNIT_OF_MEASURE_2 + offset ] )
       print ( "units  2    " + str( varlist[ constants.POINT_REPLY_UNIT_OF_MEASURE_2 + offset] ) + "  " + ChannelTypeAsString )
       ChannelTypeAsString = utils.DecodeChannelType( varlist[ constants.POINT_REPLY_UNIT_OF_MEASURE_3 + offset ] )
       print ( "units  3    " + str( varlist[ constants.POINT_REPLY_UNIT_OF_MEASURE_3 + offset] ) + "  " + ChannelTypeAsString)
       
       DisplayReadingAsString = utils.DecodeAnalogueValueToHuman( varlist[ constants.POINT_REPLY_UNIT_OF_MEASURE_1 + offset], varlist[ constants.POINT_REPLY_CONVERTED_VALUE_1 + offset ] )
       print ( "Conv 1      " + str( varlist[ constants.POINT_REPLY_CONVERTED_VALUE_1 + offset ] ) + "  " + DisplayReadingAsString )
       DisplayReadingAsString = utils.DecodeAnalogueValueToHuman( varlist[ constants.POINT_REPLY_UNIT_OF_MEASURE_2 + offset], varlist[ constants.POINT_REPLY_CONVERTED_VALUE_2 + offset ] )
       print ( "Conv 2      " + str( varlist[ constants.POINT_REPLY_CONVERTED_VALUE_2 + offset ] ) + "  " + DisplayReadingAsString)
       DisplayReadingAsString = utils.DecodeAnalogueValueToHuman( varlist[ constants.POINT_REPLY_UNIT_OF_MEASURE_3 + offset], varlist[ constants.POINT_REPLY_CONVERTED_VALUE_3 + offset ] )
       print ( "Conv 3      " + str( varlist[ constants.POINT_REPLY_CONVERTED_VALUE_3 + offset ] ) + "  " + DisplayReadingAsString )
       
       InstantAlarmStateAsString = utils.DecodeAlarmState( varlist[ constants.POINT_REPLY_INSTANT_ACTIVE + offset] )
       print ( "now Alarm   " + str( varlist[ constants.POINT_REPLY_INSTANT_ACTIVE + offset ] ) + "   " + InstantAlarmStateAsString )
       print ( "now Fault   " + str( varlist[ constants.POINT_REPLY_INSTANT_FAULT + offset ] ) )
       
       ConfirmedAlarmStateAsString = utils.DecodeAlarmState( varlist[ constants.POINT_REPLY_CONFIRMED_ACTIVE + offset] )
       print ( "Confirm Alm " + str( varlist[ constants.POINT_REPLY_CONFIRMED_ACTIVE + offset ] ) + "   " + ConfirmedAlarmStateAsString )
       print ( "Confirm Flt " + str( varlist[ constants.POINT_REPLY_CONFIRMED_FAULT + offset ] ) )
       
       AckedAlarmStateAsString = utils.DecodeAlarmState( varlist[ constants.POINT_REPLY_ACKED_ACTIVE + offset] )
       print ( "Acked Alm   " + str( varlist[ constants.POINT_REPLY_ACKED_ACTIVE + offset ] ) + "   " + AckedAlarmStateAsString )
       print ( "Acked Flt   " + str( varlist[ constants.POINT_REPLY_ACKED_FAULT + offset ] ) )
       
       print ( "OP Is Forced" + str( varlist[ constants.POINT_REPLY_IS_OUTPUT_FORCED + offset ] ) )
       print ( "OP Unforced " + str( varlist[ constants.POINT_REPLY_OUTPUT_UNFORCED_STATE + offset ] ) )
       print ( "OP Forced   " + str( varlist[ constants.POINT_REPLY_OUTPUT_FORCED_STATE + offset ] ) )

       print ( "Client Key 1 " + str( varlist[ constants.POINT_REPLY_CLIENT_KEY_1 + offset ] ) )
       print ( "Client Key 2 " + str( varlist[ constants.POINT_REPLY_CLIENT_KEY_2 + offset ] ) )

    
       print ( "----" )
   
    
def decode_panel_info_reply( packet_to_decode ) :     
    
    global point_poll_sucess
    global use_mxspeak_6;
    
    point_poll_sucess = True

    length = len( packet_to_decode )


    # remove checksum from end
    # length of comma plus last characters may vary
    #shorter = packet_to_decode[:length - 3]
    shorter = packet_to_decode.strip(',\n')

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
    
    # print( print_me )
    
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
       
    elif ( PacketID == constants.PACKET_ID_PANEL_INFORMATION ) : 
      decode_panel_info_reply( packet_to_decode ) 
      
    else :
      print ( "Reply Packet Type " + str( varlist[ constants.OFFSET_FOR_PACKET_TYPE_MXSPEAK_6 ] ) )


def FormRequestPacket( node_number, loop, is_first_point  ) :

    # print( "node number " + str( node_number ))


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
    #                        L  SIG DN SN DCH  DT SCH  STSK MK PKT RS   \/ packet is here
    #                                                                   The packet contents is different for MXSpeak 5 and 6
    #SamplePacket_mxspeak6 = "58,228,0, 0, 0,  4,  253, 146, 0, 148,0,  12,1,0,1,0,  254,0,0,1,3,0,0,3,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,0,10"
    #                                                                                254 - loginal zone
    #                                                                                    0 - dcevice category any
    #                                                                                      0,1 - group - dont care
    #                                                                                          3 - output states any
    #                                                                                            0,0 - unused
    SamplePacket_mxspeak6  = "58,228,0, 0, 0,  4,  253, 146, 0, 148,0,  12,1,0,1,0,  254,0,0,1,3,0,0,3,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,1,10"
    #SamplePacket_mxspeak5 = "57    ,0, 0, 0,  1,    0,   0, 0, 148,   0 ,0,1,0,1,0,254,0,0,1,3,0,0,3,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,0,10"
    #SamplePacket_mxspeak5 = "57    ,0, 0, 0,  1,    0,   0, 0, 148,   0 ,0,1,0,1,0,254,0,0,1,3,0,0,3,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,1,10"
    SamplePacket_mxspeak5 = "57    ,0, 0, 0,  1,    0,   0, 0, 148,   0 ,0,1,0,1,0,254,0,0,1,3,0,0,3,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,1,10"


    global glb_point_info_client_number
    global ptp_sequence
    global use_mxspeak_6
                                                   
    #                             DN CH DCH DT  SCH  ST MK PKT  RS  \/ client code here                                                   
    NextPacket_mxspeak6 = "14,228,0, 0, 0,  4,  0,   0, 0, 150,  0, 0, 0, 0"
    NextPacket_mxspeak5 = "11,    0, 0 ,0,  1,  0,   0,    123,150 ,0, 0"

    glb_reply_indicates_no_more_points_on_loop = False

    if ( use_mxspeak_6 ) : 
        #print( "USING MXSPEAK 6")
        if ( is_first_point == True ) : 
            varlist = map(int, SamplePacket_mxspeak6 .split(','));
        else : 
            varlist = map(int, NextPacket_mxspeak6 .split(','));

    else : 
        #print( "USING MXSPEAK 5")
        if ( is_first_point == True ) : 
            varlist = map(int, SamplePacket_mxspeak5 .split(','));
        else : 
            varlist = map(int, NextPacket_mxspeak5 .split(','));

    detail_display = 0
    
    # to be on the safe side
    # check the packet type.
    
    if ( use_mxspeak_6 ) : 

        # if the point is NOT 1, then we will not be using the full request packet
        # we will be using the 'next' packet.
        if ( varlist[ constants.OFFSET_FOR_PACKET_TYPE_MXSPEAK_6 ] == constants.PACKET_ID_POINT_INFO_REQUEST ) : 
        
            varlist[ constants.POINT_INFO_REQUEST_HEADER_DESTINATION_NODE ] = node_number
        
            varlist[ constants.POINT_INFO_REQUEST_POINT_OFFSET ] = 255
            varlist[ constants.POINT_INFO_REQUEST_LOOP_OFFSET  ] = loop

            varlist[ constants.POINT_INFO_REQUEST_NODE_OFFSET ] = node_number
            
            if ( config.DISPLAY_POINT_REQUEST_PACKETS_OVERVIEW == 1 ) :
                print( "\nRequest -  Node : " + str(node_number) + " Loop : " + str( loop ) + ",  Point : " + str( point ) )            

                if ( config.DISPLAY_POINT_REQUEST_PACKETS_DETAIL == 1 ) :
                   print ( "Point Information Request : Node      " + str(  varlist[ constants.POINT_INFO_REQUEST_NODE_OFFSET ] ) )
                   print ( "Point Information Request : channel   " + str(  varlist[ constants.POINT_INFO_REQUEST_CHANNEL_OFFSET ] )  + "   MXSpeak 6 12 is main processor")
                   print ( "Point Information Request : chan addr " + str(  varlist[ constants.POINT_INFO_REQUEST_LOOP_OFFSET ] )  + "   Channel 12, channel addr 1 = loop A")
                   print ( "Point Information Request : pnt cat   " + str(  varlist[ constants.POINT_INFO_REQUEST_POINT_CATEGORY_OFFSET ] )  + "   0 - real points")
                   print ( "Point Information Request : pnt addr  " + str(  varlist[ constants.POINT_INFO_REQUEST_POINT_OFFSET ] ) )
                   print ( "Point Information Request : log pt 1  " + str(  varlist[ constants.POINT_INFO_REQUEST_LOGICAL_ADDR_PT1_OFFSET ] ) )
                   print ( "Point Information Request : log pt 2  " + str(  varlist[ constants.POINT_INFO_REQUEST_LOGICAL_ADDR_PT2_OFFSET ] ) )
                   print ( "Point Information Request : dev cat   " + str(  varlist[ constants.POINT_INFO_REQUEST_DEVICE_CATEGORY_OFFSET ] ) )


        if ( varlist[ constants.OFFSET_FOR_PACKET_TYPE_MXSPEAK_6 ] == constants.PACKET_ID_POINT_INFO_NEXT_REQUEST ) : 
        
            varlist[ constants.POINT_INFO_REQUEST_HEADER_DESTINATION_NODE ] = node_number
            varlist[ constants.POINT_INFO_NEXT_REQUEST_CLIENT_CODE_1 ] = 0 
            varlist[ constants.POINT_INFO_NEXT_REQUEST_CLIENT_CODE_2  ] = glb_point_info_client_number
        
            print( "NOW HERE : Client code is "+ str(glb_point_info_client_number) )
            if ( config.DISPLAY_POINT_REQUEST_PACKETS_OVERVIEW == 1 ) :
                print( "\nNext request : Cient code  : " + str(glb_point_info_client_number) )    


    else :
        # MXSPEAK 5
        #
        #
        if ( varlist[ constants.OFFSET_FOR_PACKET_TYPE_MXSPEAK_5 ] == constants.PACKET_ID_POINT_INFO_REQUEST ) : 

            #varlist[ constants.POINT_INFO_REQUEST_POINT_OFFSET_MXSPEAK_5 ] = point
            #varlist[ constants.POINT_INFO_REQUEST_LOOP_OFFSET_MXSPEAK_5  ] = loop
            
            varlist[ constants.POINT_INFO_REQUEST_POINT_OFFSET_MXSPEAK_5 ] = 255
            varlist[ constants.POINT_INFO_REQUEST_LOOP_OFFSET_MXSPEAK_5  ] = loop
            varlist[ constants.POINT_INFO_REQUEST_HEADER_DESTINATION_NODE_MXSPEAK5 ] = node_number
            
        if ( varlist[ constants.OFFSET_FOR_PACKET_TYPE_MXSPEAK_5 ] == constants.PACKET_ID_POINT_INFO_NEXT_REQUEST ) : 
        
            varlist[ constants.POINT_INFO_NEXT_REQUEST_CLIENT_CODE_1_MXPEAK5 ] = 0 
            varlist[ constants.POINT_INFO_NEXT_REQUEST_CLIENT_CODE_2_MXPEAK5 ] = glb_point_info_client_number
            #varlist[ constants.POINT_INFO_REQUEST_HEADER_DESTINATION_NODE_MXSPEAK5    ] = node_number
        
        
            if ( config.DISPLAY_POINT_REQUEST_PACKETS_OVERVIEW == 1 ) :
                print( "\nNext request : Cient code  : " + str(glb_point_info_client_number) )    


    # Start with SOH and low level sequence number.
    result = "1" # + str ( ptp_sequence )

    # Add the PTP sequence number to the packet.
    varlist.insert(0, ptp_sequence)

    ptp_sequence += 1
    if ptp_sequence > constants.MAX_PTP_SEQUENCE : 
     ptp_sequence = constants.MIN_PTP_SEQUENCE
    
    checksum = 0
    for el in varlist:

      checksum += el
      result += "," + str(el);

    checksum = checksum % 256

    varlist.append( checksum )

    #print( "Calculated checksum: " + str(checksum))

    result += "," + str(checksum)

    print( "Constructed Packet to send : \n" + result )

    return result 


def PointInformationScan(   ) :

    global use_mxspeak_6;
    global current_node;
    global glb_reply_indicates_no_more_points_on_loop

    # initial dealy between polls while we work out what is there.
    delaybetweenpolls = 0.3

    # Declare loop variables, with start values
    first_point_address = True
    current_loop  = 1
    current_node  = constants.MIN_NETWORK_NODE


    max_loop = constants.MAX_LOOP_TO_SCAN_MXSPEAK_5
    if ( use_mxspeak_6 == True ) : 
        max_loop = constants.MAX_LOOP_TO_SCAN_MXSPEAK_6


    while(True):

        startTime = datetime.datetime.now();
        
        #print "Packet in jobs list : \n"+content
        
        # TO DO
        # Not ideal, but adjust the packet for the loop and point address
        packettosend = FormRequestPacket( current_node, current_loop, first_point_address )
        print( "Sending request for : Node " + str( current_node )+ " Loop " + str( current_loop ) )
        
        #print(  packettosend  )

        action = "python packetizer/pointinfotest.py " + packettosend 
        #print(action)
        payload = subprocess.check_output(shlex.split(action));
        length_of_reply = len(payload)
        if length_of_reply > 1: #for some reason printing an empty payload still constitutes to greater than 0, so we use 1 instead
            # writelog(payload,logfile)
            # TODO adjust to windows 7/10
            print("Reply from Panel, Length " + str( len( payload ) ) )
            #print(payload)
            
            # If there was a NULL reply from 1-1, then we can assume the panel is not there.
            # this is different from a proper reply that indicates no point.
            if (length_of_reply == 2) :
            
                # We are not doing well.  So lets work our way out.
                glb_reply_indicates_no_more_points_on_loop = True
            
                if (( first_point_address == True ) & ( current_loop == 1)) :
                    glb_reply_indicates_no_more_points_on_loop = True
                    current_loop =  max_loop
                    print( "\n------------" )
                    print( "Nothing from this node, move to next" )
                    print( "------------\n" )
            
            if (length_of_reply > 10) :
              decode_reply_packet(payload)                
              
            #print "Payload response to serviced packet : \n"+payload; 
        else:
            #print("this is the payload" + str(payload))
            print "No device recorded for this point"

        time.sleep(delaybetweenpolls) 

        first_point_address = False
        
        # If we have got to the end of a loop.
        # start again at the start of the next loop.
        if (glb_reply_indicates_no_more_points_on_loop == True ):         
            glb_reply_indicates_no_more_points_on_loop = False
            print( "\n---------------\nMove to next loop\n----------------\n\n" )
            
            first_point_address = True

            current_loop += 1
            if (current_loop > max_loop): 
                current_loop = 1
                
                current_node += 1
                print( "\n---------------\nMove to next node\n----------------\n\n" )
                
                if (current_node > constants.MAX_NETWORK_NODE): 
                    current_node = constants.MIN_NETWORK_NODE

                   

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
    if ptp_sequence > constants.MAX_PTP_SEQUENCE : 
     ptp_sequence = constants.MIN_PTP_SEQUENCE
    
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
          decode_reply_packet(payload) 

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
            
            print "Payload response to serviced packet : \n"+payload; 
        else:
            #print("this is the payload" + str(payload))
            print "No device recorded for this point",


#
# START OF MAIN
#



delaybetweenpolls = 0.1
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
