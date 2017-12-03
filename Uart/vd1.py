import time
import threading
import serial

running = threading.Event()
running.set()
def thread_read(ser, callback=None):
    buf = b''
    while running.is_set():
        buf = read_data(ser, buf, callback)

def msg_parsed(msg_parts):
    # Do something with the parsed data
    print(msg_parsed)

ser = serial.Serial(
	port = '/dev/ttyS0',
	baudrate = 115200,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1
)
th = threading.Thread(target=thread_read, args=(ser, msg_parsed))
th.start()


# Do other stuff while the thread is running in the background
start = time.clock()
duration = 5 # Run for 5 seconds
while running.is_set():
    time.sleep(1) # Do other processing instead of sleep
#    if time.clock() > duration
#        running.clear()

th.join() # Wait for the thread to finish up and exit
ser.close() # Close the serial port
