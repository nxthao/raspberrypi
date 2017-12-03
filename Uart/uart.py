import time
import serial

ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
ser.write("Say something:")

while 1:
    rcv = ser.read(10)
    print(rcv)
    ser.write("You sent:" + repr(rcv))
    
    time.sleep(1)
