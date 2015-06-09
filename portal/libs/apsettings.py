
def makehostapdfile(ssid, passphrase, channel, orgfile, newfile):
	
	with open(orgfile) as f:
	    lines = f.readlines()
    	with open(newfile, "w") as f1:
    		f1.writelines(lines)	
    		f1.write("\nssid=" + ssid)
    		f1.write("\npassphrase=" + passphrase)
    		f1.write("\nchannel=" + channel)
