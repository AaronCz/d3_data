#!/usr/bin/python
import serial
from xbee import ZigBee

SERIALPORT = "/dev/ttyAMA0"    # the com/serial port the XBee is connected to, the pi GPIO should always be ttyAMA0
BAUDRATE = 9600      # the baud rate we talk to the xbee

ser = serial.Serial(SERIALPORT, BAUDRATE)

#Creat API object
zb = ZigBee(ser)

#this goes to a file and opens it 
file_to_send = "temperature_readings/28-00000618d8aa_temperature.csv"
file_open = open(file_to_send) 

#go through the intire file and select each line individually
with open(file_to_send) as f:
	file_contents = f.readlines()

#for loop going through each line and sendint it as one solid piece
for idx, val in enumerate(file_contents):
    	print val
	zb.send('tx', data=val, dest_addr_long='\x00\x13\xa2\x00\x40\xe2\xc6\xe2', dest_addr='\xff\xff', frame_id='\x00')

# Continuously read and print packets
while True:
    try:
	#recieve raw input from user
	info = raw_input()
	#send user input to xbee with corrosponding address
	zb.send('tx', data=info, dest_addr_long='\x00\x13\xa2\x00\x40\xe2\xc6\xe2', dest_addr='\xff\xff', frame_id='\x00')

    except KeyboardInterrupt:
        break

ser.close()