#!/usr/bin/python2
# -*- coding: utf-8 -*-
#--------------------------

#
#
# GSI 
# m.zweig 
# 23.09.2015 
# 
# 
# 
# -------------------------


import os
import sys
import getopt
import getpass

from datetime import datetime

file_host = "allTimingDevices.txt"
file_newhost = ".conf" 
myhost   = ""

detec = [["Timing","timing"],["n/a","unknown"],["Production","production"],["User","user"],["miniCS", "minics"]]
detec_all = False
debug = False

#hilfe
def help_txt():
	print "Host file extractor"
	print "it seperate timming/user/production from the main hostfile" 
	print "and generate new files."
	print "arguments are:"
	print "-t --timing      scan all timing devices"
	print "-p --production  scan all production timing devices"
	print "-u --user        scan all user timing devices"
	print "-c --minics      scan all minics timing devices"
	print "-n --unknown     scan all other timing devices"
	print "-a --all         scan all devices"
	print "-r --remove      remove all host files"	



def extract(detec):

	found_list = []
	cnt = 0

	# host file öffnen
	if debug:print "\nopen file: "+file_host

	try:
        	file_mainhost = open(file_host,"r")
	except Exception:
        	sys.exit("Failure: Cant open host main file")
        
	if debug:
        	print "...ok"
		print "\nsearching in file for :"+detec
	

	# suchen
	for line in file_mainhost:

		# suche nach gewuenschten keywort
		if detec in line:
			if debug : print ">>FOUND :"+line.strip()
			found_list.append(line.strip())
			cnt = cnt + 1

	if debug : print" Found "+str(cnt)+" items" 
	return(found_list, cnt)



# file schreiben
def write_file(dname, found, keyword):

	try:
		datei=open(dname,"w")
	except Exception:
		sys.exit("Cant write result file")

	datei.write("# Created on "+str(datetime.now())+"\n")
	datei.write("# Created from user "+getpass.getuser()+"\n")
	datei.write("# Here are all "+keyword+ " devices\n")
	datei.write("# THIS FILE IS AUTO GENERATED ! \n")
	datei.write("################################\n")

	for line in found:
		datei.write(str(line)+"\n")

	datei. close()


# host files loeschen
def remove_host():

	for element in detec:
			 
		myhost = element[1]+file_newhost	
		
		if (os.path.exists(myhost)):
			try:
				os.remove(myhost)       
			except OSError, err:
				print "FAIL: cant delete ",myhost 



# -------------------------- main ------------------------------


my_newhost = "none"
mydetec = "none" 
found = []

# argumente einlesen
try:
    myopts, args = getopt.getopt(sys.argv[1:],"hdtpucnar",["help","debug","timing","production","user","minics","unknown","all","remove"])
except getopt.GetoptError, err:
    print str(err)
    help_txt()
    sys.exit(2)


for o, arg in myopts:

	if o in("-h","--help"):
		help_txt()
		sys.exit(2)
	elif o in ("-d","--debug"):
		debug = True
	elif o in ("-t","--timing"):
		myhost = detec[0][1]+file_newhost
                mydetec = detec [0][0] 
        elif o in ("-p","--production"):
		myhost = detec[2][1]+file_newhost
                mydetec = detec [2][0]
        elif o in ("-u","--user"):
		myhost = detec[3][1]+file_newhost
                mydetec = detec [3][0]
        elif o in ("-c","--minics"):
                myhost = detec[4][1]+file_newhost
		mydetec = detec [4][0]
        elif o in ("-n","--unknown"):
		myhost = detec [1][1]+file_newhost
                mydetec = detec [1][0]
        elif o in ("-a","--all"):
                detec_all = True
		mydetec = "all"
	elif o in ("-r","--remove"):
		remove_host()
		sys.exit(2)
	else:
		help_txt()


if len(myopts) == 0:
	print "...nothing to do"
	sys.exit(2) 


# -- generate files

if detec_all:
	for element in detec:
		# host liste durchsuchen
		print "...separate "+element[0]
		found, cnt = extract(element[0])
                myhost = element[1]+file_newhost
		write_file(myhost, found, element[0])	
else:
	# host liste durchsuchen
	found, cnt = extract(mydetec)
	# ergebniss speichern
	print myhost,mydetec
	write_file(myhost, found, mydetec)
			

print "Don't forget to svn commit"
	
print "...done"






