#!/usr/bin/env python
import os
print("1-Start,2-Replay,3-Plot,4-Home,5-Record") 
val = input("Enter your value: ") 
print(val)
if(val=="1"): 
	os.system('python3 /home/uthira/rtde-2.4.8/Code.py 1')
	#continue
elif(val=="2"): 
	os.system('python3 /home/uthira/rtde-2.4.8/Code.py 2')
		#continue
elif(val=="3"): 
	os.system('python3 /home/uthira/rtde-2.4.8/Code.py 3')
		#continue
elif(val=="4"): 
	os.system('python3 /home/uthira/rtde-2.4.8/Code.py 4')
		#continue
elif(val=="5"): 
	#os.system('python3 /home/uthira/rtde-2.4.8/examples/record.py --host 127.0.0.1 --port=30004')
	os.system('python3 /home/uthira/rtde-2.4.8/examples/record.py --host 172.16.101.225 --port=30004')
		#continue


	
