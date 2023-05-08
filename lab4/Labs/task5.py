import os 
import time 
 
def ping(ip): 
  pingaling = os.popen("ping -c 1 "+ip) 
  while True: 
    line = pingaling.readline() 
    if not line:  
      break 
    if line.find('Average')>0: 
      print(ip) 
 
start = time.perf_counter() 
for host in range(1,20): 
   ip = "192.168.1."+str(host) 
   ping(ip) 
 
stop = time.perf_counter() 
print('time:',stop-start)