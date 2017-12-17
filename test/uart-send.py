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
 
print("Raspberry's sending : ")
 
try:
    while True:
        print(time.clock())
        if time.clock()>= 1:
            b = 8
            print(time.clock())
            # khi gui uart phai chuyen qua string
    	    ser.write('\xff'+'\x10'+chr(b))# chr la chuyen tu so sang string
    	    ser.flush()
    	    print("ok")
    	    time.sleep(1)
            break
except KeyboardInterrupt:
	ser.close()
