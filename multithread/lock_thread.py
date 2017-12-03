#!/usr/bin/python

import threading
import time

class myThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      print "Starting " + self.name 
      
      # Get lock to synchronize threads
      threadLock.acquire()

      #counter ban dau tro thanh delay trong ham print_time
      #counter thread1 = 1 => delay = 1,counter thread 2 = 2 => delay = 2
      print_time(self.name, self.counter, 3) 
      
      # Free lock to release next thread
      threadLock.release()

def print_time(threadName, delay, counter):
   while counter:
      time.sleep(delay)
      #print "%s: %s" % (threadName, time.ctime(time.time()))
      print('{} {}'.format(threadName, time.ctime(time.time())))
      counter -= 1

threadLock = threading.Lock()
# tao list de chua cac thread dang chay de cuoi chuong trinh biet chuong trinh nao dang chay
threads = []

# Create new threads
thread1 = myThread(1, "Thread 1", 1)
thread2 = myThread(2, "Thread 2", 2)
thread3 = myThread(3, "Thread 3", 2)

# Start new Threads
"""vi day la lap trinh da tuyen nen khi start thread1 xong( khi
start thread1 no se nhay vao run va chay ngam dinh trong chuong trinh), 
chuong trinh chinh tiep tuc nhay qua thuc hien start thread2 luon(
thread 2 tuong tu thread 1,no tiep tuc vao run va chay ngam dinh,tao thanh da tuyen dag chay) va cu tiep tuc thuc hien cac lenh duoi lenh start 2 thread
nhu lap trinh tuan tu binh thuong
"""
thread1.start()
thread2.start()
thread3.start()

print("start ok")

# Add threads to thread list
threads.append(thread1)
threads.append(thread2)
threads.append(thread3)

print("chuyen vao list ok")

# Wait for all threads to complete
for i in threads:
    i.join()
print "Exiting Main Thread"
