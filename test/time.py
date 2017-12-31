
import time

a = time.clock()

while True:
    if time.clock() >= 1:
        print time.clock()
        print(time.clock() - a)
        print("ok")
        break
 
        
