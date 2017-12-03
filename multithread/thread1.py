
import threading
import math

class WorkerThread(threading.Thread):
    def __init__(self, threadID, data):
        #cai nay de khoi tao lai threading.Thread(do minh ke thua no)
        threading.Thread.__init__(self) 
        self.threadID = threadID
        self.data = data # Initiliaze data for thread
    def run(self):
        # This method is invoked when starting a thread
        # Do the work of thread here.
        print('Thread {}: {} is running with data: {}'.format(self.threadID, self.ident, self.data))

if __name__ == '__main__':
    a = 'Thao'
    b = 'Nguyen'

    # Create thread by CheckPrimeThread
    thread1 = WorkerThread(1, a) 
    thread2 = WorkerThread(2, b)
    
    # Start threads
    thread1.start()
    thread2.start()
    
    # Wait for thread1, thread2 to terminate
    thread1.join()
    thread2.join() 
    print('Main thread exited')
