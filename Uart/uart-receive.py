#!/usr/bin/python3
 
import time
import serial
 
ser = serial.Serial(
	port = '/dev/ttyS0',
	baudrate = 115200,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1
)
 
print("Raspberry's receiving : ")
 
try:
    while True:
        a = ser.readline()
        if a == '2'
#        data = s.decode()			# decode s
#        data = data.rstrip()			# cut "\r\n" at last of string
            print("ok")				# print string
         
        if s != b'\x10\x21\x11': 
            print("don't ok") 
except KeyboardInterrupt:
	ser.close()
