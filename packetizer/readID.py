#read script 
def readID():
	f = open("panel-id.txt", "r");
	panel_id = f.readline();
	f.close;
	return panel_id;

#pid = readID();
#URL = "http://ipaddress/service.php?action=r&id=" + pid;
#print URL;


