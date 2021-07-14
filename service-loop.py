import subprocess
import shlex
import time
import datetime
import readID as readIDVar

def writelog(entry, logfile) :
    """
    writelog - write log entry to log file
    to usb drive is exists, otherwise to /tmp
    Input
        entry: string, log entry
        logfile: string, log file
    Output
        none
    """
    logdrive = ''
    out = subprocess.check_output(['ls', '/media/pi'])
    if len(out) > 0 :
        logdrive = '/media/pi/' + out
        logdrive = logdrive.rstrip('\n')
        logdrive += '/'
    else :
        logdrive = '/tmp/'
    logdrive += logfile
    fout = open(logdrive, 'a')
    fout.write(entry)
    fout.close()

def hex_to_int( value ) :

  return int( value, 16 )


def decode_point_info_reply( packet_to_decode ) : 

    length = len( packet_to_decode )

    shorter = packet_to_decode[:length - 3]

    varlist = map(hex_to_int, shorter .split(','));

    print( "\nPoint Information Reply Packet" )

    print ( "state       " + str(  varlist[ 12 ] ) + "     Zero = success")

    if ( varlist[ 12 ] == 0) : 
       print ( "Flags       " + str(  varlist[ 13 ] ) )
       print ( "Node        " + str(  varlist[ 14 ] ) )
       print ( "Channel     " + str(  varlist[ 15 ] ) )
       print ( "Chan addr   " + str(  varlist[ 16 ] ) + "    this is the loop number" )
       print ( "Pnt cat     " + str(  varlist[ 17 ] ) )
       print ( "Pnt addr    " + str(  varlist[ 18 ] ) )
       print ( "log part1   " + str(  varlist[ 19 ] ) )
       print ( "log part2   " + str(  varlist[ 20 ] ) )
       print ( "Device type " + str(  varlist[ 21 ] ) )
       print ( "Attribs     " + str(  varlist[ 22 ] ) )
       print ( "group pt1   " + str(  varlist[ 23 ] ) )
       print ( "group pt3   " + str(  varlist[ 24 ] ) )
       print ( "Area type   " + str(  varlist[ 25 ] ) )
       print ( "Area nmbr   " + str(  varlist[ 26 ] ) )
       print ( "Sector      " + str(  varlist[ 27 ] ) + "    254 if not sector")
       print ( "Loop type   " + str(  varlist[ 28 ] ) + "      1 is MX")
       print ( "raw dev id  " + str(  varlist[ 29 ] ))
 
       print ( "----" )
    
    #print( "Full packet reply : " + packet_to_decode )



def decode_reply_packet( packet_to_decode ) :

    length = len( packet_to_decode )

    shorter = packet_to_decode[:length - 3]

    varlist = map(hex_to_int, shorter .split(','));

    if ( str( varlist[ 11 ] == 149 )) : 
      decode_point_info_reply( packet_to_decode ) 
    else :
      print ( "Reply Packet Type " + str( varlist[ 11 ] ) )


def FormRequestPacket( loop, point, startpacket ) :

    # print( "Original MSG : " + startpacket )

    varlist = map(int, startpacket .split(','));

    length = len( varlist )

    display = 0
    if ( varlist[ 11 ] == 148 ) : 
       varlist[ 16 ] = point
       print( "Request Point : " + str( point ) )

    if ( display == 1 ) :
       print ( "Point Information Request : Node      " + str(  varlist[ 12 ] ) )
       print ( "Point Information Request : channel   " + str(  varlist[ 13 ] )  + "   MXSpeak 6 12 is main processor")
       print ( "Point Information Request : chan addr " + str(  varlist[ 14 ] )  + "   Channel 12, channel addr 1 = loop A")
       print ( "Point Information Request : pnt cat   " + str(  varlist[ 15 ] )  + "   0 - real points")
       print ( "Point Information Request : pnt addr  " + str(  varlist[ 16 ] ) )
       print ( "Point Information Request : log a   " + str(  varlist[ 17 ] ) )
       print ( "Point Information Request : log b   " + str(  varlist[ 18 ] ) )
       print ( "Point Information Request : dev cat " + str(  varlist[ 19 ] ) )

    else: 
       print ( "Packet Type " + str(  varlist[ 11 ] ) )

    # remove existing checksum
    varlist.pop( length -1 )
    # remove start of packet info
    varlist.pop( 0 )

    result = str ("1" )
    checksum = 0
    for el in varlist :
      checksum += el
      result += "," + str(el);

    checksum = checksum % 256

    varlist.append( checksum  )

    #print( "Calculated checksum: " + str(checksum))

    result += "," + str(checksum)

    #print( "New MSG : " + result )

    return result 


timeDelay = 1

pid = readIDVar.readID();
pid = pid.strip()
entry = "Logging Panel PI id: " + str(pid) + '\nTODO scan devices, decode packets\n'
print(entry)
f = open('packet.txt')
packets = f.readlines()

logfile = str(datetime.datetime.today().strftime('%Y%m%d%H%M%S'))
logfile += '_BlackBox.log'
# todo, adapt for Windows
print(entry)
writelog(entry, logfile)


point_address = 1
# max_point_address = 250
max_point_address = 35

while(True):

    for packet in packets :
        startTime = datetime.datetime.now();

        content =  packet #+ '\r\n' #.strip()

        #print "Packet in jobs list : \n"+content
        
        packettosend = FormRequestPacket( 1, point_address , content)

        action = "python packetizer/pointinfotest.py " + packettosend 
        #print(action)
        payload = subprocess.check_output(shlex.split(action));
        if len(payload) > 1: #for some reason printing an empty payload still constitutes to greater than 0, so we use 1 instead
            writelog(payload,logfile)
            # TODO adjust to windows 7/10
            # print("Reply from Panel")
            #print(payload)
            if (len(payload) > 10) :
              decode_reply_packet(payload) 
            #print "Payload response to serviced packet : \n"+payload; 
	else:
	    #print("this is the payload" + str(payload))
            print "No device recorded for this point",

        time.sleep(timeDelay) 

        point_address += 1
        if (point_address > max_point_address):
          point_address = 1
