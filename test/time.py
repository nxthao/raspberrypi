import time

a = time.clock()
while True:
    #print time.clock()
    if time.clock() >= 1:
        print time.clock()
        print(time.clock() - a)
        print("ok")
        break
 
        
