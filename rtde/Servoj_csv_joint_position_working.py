#!/usr/bin/env python
# coding: utf-8

import rtde_control
import sys
import rtde.csv_reader as csv_reader
import time
import pandas as pd
import numpy as np
rtde_c = rtde_control.RTDEControlInterface("127.0.0.1")# Parameters




#home
joint_q = [0,-1.57,1.57,0,1.57,3.14]
rtde_c.moveJ(joint_q,0.08,0.08,False)


with open('robot_data_record.csv') as csvfile:
    r = csv_reader.CSVReader(csvfile)
    joint_values=[r.target_q_0,r.target_q_1,r.target_q_2,r.target_q_3,r.target_q_4,r.target_q_5]  





print([joint_values[0][0],joint_values[1][0],joint_values[2][0],joint_values[3][0],joint_values[4][0],joint_values[5][0]])



rtde_c.moveJ([joint_values[0][0],joint_values[1][0],joint_values[2][0],joint_values[3][0],joint_values[4][0],joint_values[5][0]],0.08,0.08,False)




print(joint_values)
velocity = 0.001
acceleration = 0.008
dt = 0.01
lookahead_time = 0.1
gain = 300
i =0
while(1):
    start = time.time()
    rtde_c.servoJ([joint_values[0][i],joint_values[1][i],joint_values[2][i],joint_values[3][i],joint_values[4][i],joint_values[5][i]],velocity, acceleration, dt, lookahead_time, gain)    
    end = time.time()
    duration = end - start
    if duration < dt:
        time.sleep(dt - duration)
        i =i +1
rtde_c.servoStop()
rtde_c.stopScript()
    






