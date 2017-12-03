
import threading
import time

class Producer(threading.Thread):
    """
    Producers random integers to a list
    """
    def __init__(self, integers, condition, counter):
        threading.Thread.__init__(self)
        self.integers = integers
        self.condition = condition
        self.counter = counter
    
    def run(self):
        """
        Append random integers to integers list at random time.
        """
       
        while True:
            integer = random.randint(0, 256)
            self.condition.acquire()
            print('condition acquired by {}'.format(self.name))
            self.integers.append(integer)
            print('{} appended to list by {}'.format(integer, self.name))
            
            counter = self.counter.pop()
            counter += 1
            self.counter.append(counter)
            
            print('tin hieu chua xu ly {}'.format(counter))

            print('condition notified by {}'.format(self.name))
            self.condition.notify()
            
            print('condition released by {}'.format(self.name))
            self.condition.release()
            time.sleep(1)

class Consumer1(threading.Thread):
    """
    consumes random integers for a list
    """
    def __init__(self, integers, condition, counter):
        threading.Thread.__init__(self)
        self.integers = integers
        self.condition = condition
        self.counter = counter
    def run(self):
        """
        Consumes integers from shared list
        """
        while True:
            self.condition.acquire()
            print('condition acquired by {}'.format(self.name))
            while True:
                if self.integers:
                    integer = self.integers.pop()
                    print('{} popped from list by {}'.format(integer, self.name))
                    
                    counter = self.counter.pop()
                    counter -= 1
                    self.counter.append(counter)
                    print('tin hieu chua xu ly {}'.format(counter))
                    
                    break #thoat khoi vong lap

                print('conditon wait by {}'.format(self.name))
                self.condition.wait()

            print('condition released by {}'.format(self.name))
            self.condition.release()

class Consumer2(threading.Thread):
    """
    consumes random integers for a list
    """
    def __init__(self, integers, condition, counter):
        threading.Thread.__init__(self)
        self.integers = integers
        self.condition = condition
        self.counter = counter
    def run(self):
        """
        Consumes integers from shared list
        """
        while True:
            self.condition.acquire()
            print('condition acquired by {}'.format(self.name))
            while True:
                if self.integers:
                    integer = self.integers.pop()
                    print('{} popped from list by {}'.format(integer, self.name))

                    counter = self.counter.pop()
                    counter -= 1
                    self.counter.append(counter)
                    print('tin hieu chua xu ly {}'.format(counter))
                    
                    break #thoat khoi vong lap
                print('conditon wait by {}'.format(self.name))
                self.condition.wait()
            print('condition released by {}'.format(self.name))
            self.condition.release()

if __name__ == '__main__':
    # khoi tao mang intergers de thread1 tao yeu cau
    integers = []

    # so nguyen luu tru so lan tin hieu chua xu ly kip
    counter = [0]

    # day la tao 1 threading.condition moi de cac thread khac cho thong bao cua cac thread khac. co the tim hieu them qua key:"threading.Condition() in python"
    condition = threading.Condition()
    producer = Producer(integers, condition, counter)
    consumer1 = Consumer1(integers, condition, counter)
    consumer2 = Consumer2(integers, condition, counter)
    producer.start()
    consumer1.start()
    consumer2.start()
    producer.join()
    consumer1.join()
    consumer2.join()
