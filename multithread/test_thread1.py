import threading
import time
exitFlag = 0
class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Bat dau " + self.name
        print_time(self.name, self.counter, 5)
        print "Ket thuc " + self.namedef print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1# Tao cac thread moi
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)# Bat dau cac thread moi
thread1.start()
thread2.start()
print "Ket thuc Main Thread"