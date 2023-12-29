#!/usr/bin/env python
# coding: utf-8

import sys
import time
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

import numpy as np
import matplotlib.pyplot as plt
import argparse
import logging
sys.path.append('..')
import rtde_control
import rtde.rtde as rtde
import rtde.csv_reader as csv_reader
import rtde.rtde_config as rtde_config
import rtde.csv_writer as csv_writer
import os
import subprocess
import rtde.csv_binary_writer as csv_binary_writer
#rtde_c = rtde_control.RTDEControlInterface("127.0.0.1")#Simulation
rtde_c = rtde_control.RTDEControlInterface("172.16.101.225")#UR5




samples = 3000
flag1 = False
flag2 = False

def Home():	
	print("Home!")
	joint_q = [0,-1.57,1.57,0,1.57,3.14]
	rtde_c.moveJ(joint_q,0.08,0.08,False)


def Set_Freedrive():
	rtde_c.teachMode()
	print("Freedrive!")	

def Stop_Freedrive():
	rtde_c.endTeachMode()
	print("End Freedrive!")



def Replay():
	print("Replaying!")
	with open('robot_data_record.csv') as csvfile:
	    r = csv_reader.CSVReader(csvfile)
	    joint_values=[r.target_q_0,r.target_q_1,r.target_q_2,r.target_q_3,r.target_q_4,r.target_q_5]  
	
	rtde_c.moveJ([joint_values[0][0],joint_values[1][0],joint_values[2][0],joint_values[3][0],joint_values[4][0],joint_values[5][0]],0.08,0.08,False)
	print([joint_values[0][0],joint_values[1][0],joint_values[2][0],joint_values[3][0],joint_values[4][0],joint_values[5][0]])
	print(joint_values)
	
	velocity = 0.001
	acceleration = 0.008
	dt = 0.01
	lookahead_time = 0.1
	gain = 300
	i =0
	#Record_while_replay()
	
	while(i<samples):
	    start = time.time()
	    rtde_c.servoJ([joint_values[0][i],joint_values[1][i],joint_values[2][i],joint_values[3][i],joint_values[4][i],joint_values[5][i]],velocity, acceleration, dt, lookahead_time, gain)    
	    end = time.time()
	    duration = end - start
	    if duration < dt:
	        time.sleep(dt - duration)
	    i =i +1
	rtde_c.servoStop()
	rtde_c.stopScript()
	print("Replay done!")
	    

def Plot_same_file():
	print("Plotting!")
	with open('robot_data_record.csv') as csvfile:
	    r = csv_reader.CSVReader(csvfile)
	    cartesian_values_record=[r.actual_TCP_pose_0,r.actual_TCP_pose_1,r.actual_TCP_pose_2,r.actual_TCP_pose_3,r.actual_TCP_pose_4,r.actual_TCP_pose_5]      
	    print(cartesian_values_record)
	fig = go.Figure()
	Plot1 = go.Scatter3d(x = cartesian_values_record[0],
		              y = cartesian_values_record[1],
		              z = cartesian_values_record[2],                  
		              marker=dict(
		              size=1,
		              color='blue',               
		              colorscale='Viridis',  
		              line=dict(width=1,color='lightblue'),
		            opacity=1))

	with open('robot_data_replay.csv') as csvfile:
	    r = csv_reader.CSVReader(csvfile)
	    cartesian_values_replay=[r.actual_TCP_pose_0,r.actual_TCP_pose_1,r.actual_TCP_pose_2,r.actual_TCP_pose_3,r.actual_TCP_pose_4,r.actual_TCP_pose_5]      
	    print(cartesian_values_replay)
	Plot2 = go.Scatter3d(x = cartesian_values_replay[0],
		              y = cartesian_values_replay[1],
		              z = cartesian_values_replay[2],                  
		              marker=dict(
		              size=1,
		              color='red',               
		              colorscale='Viridis',  
		              line=dict(width=1,color='olive'),
		              opacity=1))
		             
	fig.add_trace(Plot1)	
	fig.add_trace(Plot2)
	fig.show()  
	print("Plotted!")
	fig.write_html("Record_Replay_plot.html")
	

def Plot_diff_file():
	print("Plotting!")
	with open('robot_data_record.csv') as csvfile:
	    r = csv_reader.CSVReader(csvfile)
	    cartesian_values_record=[r.actual_TCP_pose_0,r.actual_TCP_pose_1,r.actual_TCP_pose_2,r.actual_TCP_pose_3,r.actual_TCP_pose_4,r.actual_TCP_pose_5]      
	    print(cartesian_values_record)
	fig = go.Figure()
	Plot1 = go.Scatter3d(x = cartesian_values_record[0],
		              y = cartesian_values_record[1],
		              z = cartesian_values_record[2],                  
		              marker=dict(
		              size=1,
		              color='blue',               
		              colorscale='Viridis',  
		              line=dict(width=1,color='lightblue'),
		            opacity=1))

	with open('robot_data_replay.csv') as csvfile:
	    r = csv_reader.CSVReader(csvfile)
	    cartesian_values_replay=[r.actual_TCP_pose_0,r.actual_TCP_pose_1,r.actual_TCP_pose_2,r.actual_TCP_pose_3,r.actual_TCP_pose_4,r.actual_TCP_pose_5]      
	    print(cartesian_values_replay)
	Plot2 = go.Scatter3d(x = cartesian_values_replay[0],
		              y = cartesian_values_replay[1],
		              z = cartesian_values_replay[2],                  
		              marker=dict(
		              size=1,
		              color='red',               
		              colorscale='Viridis',  
		              line=dict(width=1,color='olive'),
		              opacity=1))
		             
	fig.add_trace(Plot1)
	fig.show()
	fig2= go.Figure()
	fig2.add_trace(Plot2)
	fig2.show()  
	print("Plotted!")
	fig.write_html("Record_plot.html")
	fig2.write_html("Replay_plot.html")

def Record_while_replay():
	
	command = "./record.sh" + " & pid=$!;sleep " + str(1) + "; kill -9 $pid"
	subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	
def Plot():
	while(1):
		print("Do you want to plot the record file and replay file? ")
		var = input("A- Single File, B - Two Different files,  Any other key - Exit")
		if(var =="A"):
			Plot_same_file()			
		elif(var == "B"):
			Plot_diff_file()			
		else:			
			break
def Record_while_freedrive():
	print('1')
	os.system('python3 record.py --host=172.16.101.225 --port=30004 --samples 3000 --output robot_data_record.csv')

def main():	
	if(rtde_c.isConnected()):
		rtde_c.disconnect()
		rtde_c.reconnect()
	while(1):		
		try:
			
			print("1-Recording,2-Replaying,3-Home,4- Plot Menu,Any other key - Exit") 
			val = input("Enter your value: ") 								
			if(val== "1"):
				print("Starting with Recording!")				
				rtde_c.teachMode()
				print("..")
				Record_while_freedrive()	
				rtde_c.endTeachMode()
				print('Done with Recording!')
				flag1 = True								
			elif(val == "2"):	
				Record_while_replay()					
				Replay()				
				print('Replaying')	
				flag2 = True			
			elif(val == "3"):			
				Home()	
			elif(val == '4'):
				Plot()	
			else:
				exit
					    
		except KeyboardInterrupt:	
			rtde_c.disconnect()
		

		rtde_c.disconnect()							
		
	
		
main()
