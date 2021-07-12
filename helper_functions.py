import time
f = open('packet.txt')
lines = f.readlines()
while(True) :
    for line in lines :
        print(line.strip())
        time.sleep(1)
    print('finito')
    time.sleep(1)

