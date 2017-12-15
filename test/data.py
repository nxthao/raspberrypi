
import threading
import time
import serial
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
account_sid = " "
auth_token = " "
client_sms = Client(account_sid, auth_token)

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
       
        while True:
            try:
                while True:
                    a = ser.read()
                    if a == '\xff':
                        #wait to receive data from uart
                        #dung time.sleep de cho lay het du lieu 1 lan truyen
                        time.sleep(0.003)
                        #doc du lieu dua vao b
                        b = ser.read(ser.inWaiting())
                        """ in gia tri hexa cua a,
                        (chi cach nay in duoc gtri hexa cua string)
                        """
                        #gia tri c chinh la gia tri toan bo data minh nhan dc
                        c = a + b[0] + b[1] + b[2] + b[3] + b[4] + b[5]
                        print " ".join(hex(ord(n)) for n in a)
                        print " ".join(hex(ord(n)) for n in b)
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
                                    self.data.insert(0, c[i])
                                    i += 1 
                                print(" data send ok \n")
                                break
                            else:
                                print(" data send don't ok \n")
                                # sau do no se quay lai nhan data tu uart

            # de bat khi khong nhan duoc du lieu
            # (thong qua bat loi khong co chi so trong mang)

            except IndexError as e:
                print (e)
                # lenh continue de bo qua cac lenh sau no va cho lai vong lap
                continue


            self.condition.acquire()
            print('condition acquired by {}'.format(self.name))

            # print('{} appended to list by {}'.format(self.data, self.name))
            print " ".join(hex(ord(n)) for n in self.data)
            
            counter = self.counter.pop()
            counter += 1
            self.counter.append(counter)
            
            print('tin hieu chua xu ly {}'.format(counter))

            print('condition notified by {}'.format(self.name))
            self.condition.notify()
            
            print('condition released by {}'.format(self.name))
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
                                print('condition acquired by {}'.format(self.name))

                                # tao vong lap de nhan gia tri
                                n = 0
                                while n <= 6:
                                    self.data.insert(0, b[m + n])
                                    n += 1      
                                #print('{} appended to list by {}'.format(self.data, self.name))
                                print " ".join(hex(ord(n)) for n in self.data)
            
                                counter = self.counter.pop()
                                counter += 1
                                self.counter.append(counter)
            
                                print('tin hieu chua xu ly {}'.format(counter))

                                print('condition notified by {}'.format(self.name))
                                self.condition.notify()
            
                                print('condition released by {}'.format(self.name))
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
            print('condition acquired by {}'.format(self.name))
            data_t = []
            while True:
                if self.data:
                    # tao vong lap nhan gia tri
                    i = 0
                    while i <= 6:
                        t = self.data.pop()
                        data_t.append(t)
                        i += 1

                    #print('{} popped from list by {}'.format(data_t, self.name))
                    print " ".join(hex(ord(n)) for n in data_t)
                    
                    counter = self.counter.pop()
                    counter -= 1
                    self.counter.append(counter)
                    print('tin hieu chua xu ly {}'.format(counter))
                    
                    break #thoat khoi vong lap

                print('conditon wait by {}'.format(self.name))
                self.condition.wait()

            print('condition released by {}'.format(self.name))
            self.condition.release()

            # kiem tra xem phai tiva gui khong
           
            if data_t[1] == '\x10':
                # kiem tra xem nhiet do hay do am 
                if data_t[2] == '\x24':
                    print("xu ly data nhiet do")
                    temp = float(ord(data_t[4]))

                    # dua data nhiet do vao infuxdb
                    print("gia tri: {}".format(temp))
                    json_body = [
                        {
                            "measurement": "sensor",
                            "fields": {
                                "value": temp,
                            }
                        }
                    ]
                    
                    client.write_points(json_body) # viet data tu json den InfluxDB

                    # neu nhiet do qua lon se gui sms ve phone
                    if ord(data_t[4]) >= 88:
                        client_sms.messages.create(
                            to="+841655240171",
                            from_="+13342125125",
                            body="HELLO THAO NGUYEN"
                        )
                         

                elif data_t[2] == '\x25':
                    print("xu ly data do am") 
                    humidity = float(ord(data_t[4]))

                    # dua data do am vao infuxdb
                    print("gia tri: {}".format(humidity))
                    json_body = [
                        {
                            "measurement": "sensor1",
                            "fields": {
                                "value": humidity,
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
