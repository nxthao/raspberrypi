
import threading
import time
import serial
import RPi.GPIO as GPIO
from PyCRC.CRC16 import CRC16
from influxdb import InfluxDBClient
from twilio.rest import Client


# cai dat thong so uart
ser = serial.Serial(
        port = '/dev/ttyS0',
        baudrate = 115200,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
)

# cai dat thong so infuxdb
host = "192.168.1.8"
port = "8086"
dbname = "demo"  #tao database
client = InfluxDBClient(host=host, port=port, database=dbname) # tao object InfluxDB 


# cai dat thong so twilio
account_sid = ""
auth_token = ""
client_sms = Client(account_sid, auth_token)

# cai dat thong so GPIO
GPIO.setmode(GPIO.BCM)
led = 4
GPIO.setup(led, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)#dien tro keo xuong cho led

class Producer(threading.Thread):
    """
    Producers will receive data from uart
    """
    def __init__(self, data, condition, counter):
        threading.Thread.__init__(self)
        self.data = data
        self.condition = condition
        self.counter = counter
    
    def run(self):
        """
        Append random data to data list at random time.
        """
       
        state_previous = False

        while True:
            t = time.clock() 
            try:
                while True:
                    #kiem tra led
                    state = GPIO.input(led)
                    if state == True:
                        if state_previous == False:
                            ser.write('\x10'+'\x21'+'\x11'+'\xD9'+'\x99')
                            state_previous = state
                            print("bat led")  
                    elif state == False:
                        if state_previous == True:
                            ser.write('\x10'+'\x21'+'\x00'+'\x19'+'\x95')
                            state_previous = state
                            print("tat led")


                    a = ser.read()
                    if a == '\xff':
                        #wait to receive data from uart
                        #dung time.sleep de cho lay het du lieu 1 lan truyen
                        time.sleep(0.003)
                        """
                        doc du lieu dua vao b(b la tat ca du lieu uart gui
                        ,ngoai tru a)
                        """
                        b = ser.read(ser.inWaiting())
                        print " ".join(hex(ord(n)) for n in b)
                        
                        #gia tri c chinh la gia tri toan bo data minh nhan dc
                        c = a + b[0] + b[1] + b[2] + b[3] + b[4] + b[5]
                        print " ".join(hex(ord(n)) for n in c)
                        data_t = [] 

                        # kiem tra xem nhan du data khong 
                        if ord(b[5]):
                            """ kiem tra xem nhan dung data 
                            gui tu tiva khong
                            """ 
                            data_crc = c
                            test_crc = (CRC16().calculate(data_crc))
                            if test_crc == 0:
                                i = 0
                                while i <= 6:  
                                    #dua du lieu vao data,nhung dua kieu insert
                                    self.data.insert(0, c[i])
                                    i += 1 
                                print(" data send ok \n")
                                break
                            else:
                                print(" data send don't ok \n")
                                # sau do no se quay lai nhan data tu uart
                          
                    #print(time.clock())
                    time.sleep(1)
                    if (time.clock() - t) >= 20:
                        ser.write('\x10'+'\x26'+'\xFF'+'\x5B'+'\xE5')


            # de bat khi khong nhan duoc du lieu
            # (thong qua bat loi khong co chi so trong mang)

            except IndexError as e:
                print (e)
                state_previous = state
                # lenh continue de bo qua cac lenh sau no va cho lai vong lap
                continue


            self.condition.acquire()
            
            counter = self.counter.pop()
            counter += 1
            self.counter.append(counter)
            
            print('tin hieu chua xu ly {}'.format(counter))

            self.condition.notify()
            
            self.condition.release()
            time.sleep(1)

            # kiem tra xem co data gui lien tiep nhau ko
            m = 6
            try:
                while m < 20:
                    """ data gui tu uart se duoc luu tat ca trong b
                        vi vay se kiem tra trong b
                    """
                    if b[m] == '\xff':
                        if ord(b[m + 6]):
                            # kiem tra xem nhan dung data gui tu tiva
                            data_crc2 = b[m] + b[m+1] + b[m+2] + b[m+3] + b[m+4] + b[m+5] + b[m+6]
                            test_crc2 = (CRC16().calculate(data_crc2))
                            if test_crc2 == 0:
                            
                                self.condition.acquire()

                                # tao vong lap de nhan gia tri
                                n = 0
                                while n <= 6:
                                    self.data.insert(0, b[m + n])
                                    n += 1      
            
                                counter = self.counter.pop()
                                counter += 1
                                self.counter.append(counter)
            
                                print('tin hieu chua xu ly {}'.format(counter))

                                self.condition.notify()
            
                                self.condition.release()

                                print(" data 2 send ok \n")
                                break;
                            else:
                                print(" data  2 send don't ok \n")      
                    m += 1

            # de bat khi khong nhan duoc du lieu
            # (thong qua bat loi khong co chi so trong mang)

            except IndexError as e:
                print (e)
                state_previous = state


class Consumer1(threading.Thread):
    """
    it will receive data from producer
    """
    def __init__(self, data, condition, counter):
        threading.Thread.__init__(self)
        self.data = data
        self.condition = condition
        self.counter = counter
    def run(self):
        """
        it will receive data from producer
        """
        while True:
            self.condition.acquire()
            data_t = []
            while True:
                if self.data:
                    # tao vong lap nhan gia tri
                    i = 0
                    while i <= 6:
                        t = self.data.pop()
                        data_t.append(t)
                        i += 1

                    print " ".join(hex(ord(n)) for n in data_t)
                    
                    counter = self.counter.pop()
                    counter -= 1
                    self.counter.append(counter)
                    print('tin hieu chua xu ly {}'.format(counter))
                    
                    break #thoat khoi vong lap

                self.condition.wait()

            self.condition.release()

                  
            # kiem tra xem phai tiva gui khong
           
            if data_t[1] == '\x10':
                # kiem tra xem nhiet do hay do am 
                if data_t[2] == '\x24':
                    print("xu ly data nhiet do")
                    temp1 = float(ord(data_t[4]))

                    # dua data nhiet do vao infuxdb
                    print("gia tri: {}".format(temp1))
                    json_body = [
                        {
                            "measurement": "temperature_1",
                            "fields": {
                                "value": temp1,
                            }
                        }
                    ]
                    
                    client.write_points(json_body) # viet data tu json den InfluxDB

                    # neu nhiet do qua lon se gui sms ve phone
                    if ord(data_t[4]) >= 300:
                        client_sms.messages.create(
                            to="+841655240171",
                            from_="+13342125125",
                            body="canh bao! nhiet do thu duoc qua cao "
                        )
                         

                elif data_t[2] == '\x25':
                    print("xu ly data do am") 
                    humidity1 = float(ord(data_t[4]))

                    # dua data do am vao infuxdb
                    print("gia tri: {}".format(humidity1))
                    json_body = [
                        {
                            "measurement": "humidity_1",
                            "fields": {
                                "value": humidity1,
                            }
                        }
                    ]
                    
                    client.write_points(json_body) # viet data tu json den InfluxDB
                 
                elif data_t[2] == '\x23':
                    print("xu ly data anh sang") 
                    light1_temp = ord(data_t[3])*16*16 + ord(data_t[4])
                    light1 = round(float(light1_temp / 1.2), 2)

                    # dua data anh sang vao infuxdb
                    print("gia tri: {}".format(light1))
                    json_body = [
                        {
                            "measurement": "light_1",
                            "fields": {
                                "value": light1,
                           }
                        }
                    ]
                    
                    client.write_points(json_body) # viet data tu json den InfluxDB
                
                elif data_t[2] == '\x27':
                    print("xu ly data khong khi") 
                    k1 = float(ord(data_t[4]))

                    # dua data khong khi vao infuxdb
                    print("gia tri: {}".format(k1))
                    json_body = [
                        {

                            "measurement": "khong_khi_1",
                            "fields": {
                                "value": k1,
                            }
                        }
                    ]
                    
                    client.write_points(json_body) # viet data tu json den InfluxDB
                    print("xu ly xong tram 1 \n \n ") 

            elif data_t[1] == '\x20':
                # kiem tra xem nhiet do hay do am 
                if data_t[2] == '\x24':
                    print("xu ly data nhiet do tram 2")
                    temp_2 = float(ord(data_t[4]))

                    # dua data nhiet do vao infuxdb
                    print("gia tri: {}".format(temp_2))
                    json_body = [
                        {
                            "measurement": "temperature_2",
                            "fields": {
                                "value": temp_2,
                            }
                        }
                    ]
                    
                    client.write_points(json_body) # viet data tu json den InfluxDB

                    # neu nhiet do qua lon se gui sms ve phone
                    if ord(data_t[4]) >= 100:
                        client_sms.messages.create(
                            to="+841655240171",
                            from_="+13342125125",
                            body="nhiet do qua cao"
                        )
                         

                elif data_t[2] == '\x25':
                    print("xu ly data do am tram 2") 
                    humidity_2 = float(ord(data_t[4]))

                    # dua data do am vao infuxdb
                    print("gia tri: {}".format(humidity_2))
                    json_body = [
                        {
                            "measurement": "humidity_2",
                            "fields": {
                                "value": humidity_2,
                            }
                        }
                    ]
                    
                    client.write_points(json_body) # viet data tu json den InfluxDB
                elif data_t[2] == '\x23':
                    print("xu ly data anh sang tram 2") 
                    light2_temp = ord(data_t[3])*16*16 + ord(data_t[4])
                    light2 = round(float(light2_temp / 1.2), 2)

                    # dua data anh sang vao infuxdb
                    print("gia tri: {}".format(light2))
                    json_body = [
                        {
                            "measurement": "light_2",
                            "fields": {
                                "value": light2,
                           }
                        }
                    ]
                    client.write_points(json_body) # viet data tu json den InfluxDB
                elif data_t[2] == '\x27':
                    print("xu ly data khong khi") 
                    k2 = float(ord(data_t[4]))

                    # dua data khong khi vao infuxdb
                    print("gia tri: {}".format(k2))
                    json_body = [
                        {

                            "measurement": "khong_khi_2",
                            "fields": {
                                "value": k2,
                            }
                        }
                    ]
                    
                    client.write_points(json_body) # viet data tu json den InfluxDB

if __name__ == '__main__':
    # khoi tao mang intergers de thread1 tao yeu cau
    data = []

    # so nguyen luu tru so lan tin hieu chua xu ly kip
    counter = [0]

    # day la tao 1 threading.condition moi de cac thread khac cho thong bao cua cac thread khac. co the tim hieu them qua key:"threading.Condition() in python"
    condition = threading.Condition()
    producer = Producer(data, condition, counter)
    consumer1 = Consumer1(data, condition, counter)
    producer.start()
    consumer1.start()
    producer.join()
    consumer1.join()
