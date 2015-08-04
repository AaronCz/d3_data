#!/usr/bin/python
import serial, os, difflib
from xbee import ZigBee
from difflib import *

SERIALPORT = "/dev/ttyAMA0"    # the com/serial port the XBee is connected to, the pi GPIO should always be ttyAMA0
BAUDRATE = 9600      # the baud rate we talk to the xbee

ser = serial.Serial(SERIALPORT, BAUDRATE)

#Creat API object
zb = ZigBee(ser)

#this goes to a file directory and and opens it 
file = "temperature_readings/28-00000618d8aa_temperature.csv"

#select only the filename from selected directory by taking the last part element
filename = file.split('/')
filename = filename[-1]
#sending file name
zb.send('tx', data=filename, dest_addr_long='\x00\x13\xa2\x00\x40\xe2\xc6\xe2', dest_addr='\xff\xff', frame_id='\x00')

#create a water to check file of first file
watcher = os.stat(file)
last_modified = watcher.st_mtime

#go through the intire file and select each line individually
with open(file) as f:
	current_file = f.readlines()

#wait for response to continue (need to fix)	
#print ("waiting")
#response = zb.wait_read_frame()
#print response
#print ("received")

#for loop going through each line and sending it to specific xbee using address
for idx, val in enumerate(current_file):
#    	print val
	zb.send('tx', data=val, dest_addr_long='\x00\x13\xa2\x00\x40\xe2\xc6\xe2', dest_addr='\xff\xff', frame_id='\x00')

#setting variable for initial file tracking	
c_file = open(file)

# Continuously read and print packets
while True:
    try:

	#keep watching until change has been found
	watcher = os.stat(file)
	this_modified = watcher.st_mtime

	#if the file has been modified preform actions
	if this_modified > last_modified:
		last_modified = this_modified
		updated_file = open(file)

		print ("modified")

		#go through updatef file line by line
		with  updated_file as g:
    			glines = g.readlines()
	
			#compares the old file with the modified file
    			d = difflib.Differ()
    			diff = list(d.compare(current_file, glines))
    			#print("\n".join(diff))
			
			#goes through lines of 'diff'
			difference = ""
			for line in diff:
 				 if line[0] == '+':
    				  difference += line
	
			#send updated line and update file
			zb.send('tx', data=difference, dest_addr_long='\x00\x13\xa2\x00\x40\xe2\xc6\xe2', dest_addr='\xff\xff', frame_id='\x00')
			c_file = updated_file

    except KeyboardInterrupt:
        break

ser.close()