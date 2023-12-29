#!/usr/bin/env python
# coding: utf-8


import sys
import time
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
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
import rtde.csv_binary_writer as csv_binary_writer
rtde_c = rtde_control.RTDEControlInterface("127.0.0.1")#Simulation
#rtde_c = rtde_control.RTDEControlInterface("172.16.101.225")#UR5


	

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
	
		
	host ='127.0.0.1'
	port =30004
	samples =5000
	frequency =125
	config = '/home/uthira/rtde-2.4.8/examples/record_configuration.xml'
	output = 'robot_data_replay.csv'
	verbose = False
	binary = False
	if verbose:
		logging.basicConfig(level=logging.INFO)

	conf = rtde_config.ConfigFile(config)
	output_names, output_types = conf.get_recipe('out')

	con = rtde.RTDE(host, port)
	con.connect()
	print("Replaying!")
	with open('robot_data_record.csv') as csvfile:
		r = csv_reader.CSVReader(csvfile)
		joint_values=[r.target_q_0,r.target_q_1,r.target_q_2,r.target_q_3,r.target_q_4,r.target_q_5]  

	
	rtde_c.moveJ([joint_values[0][0],joint_values[1][0],joint_values[2][0],joint_values[3][0],joint_values[4][0],joint_values[5][0]],0.08,0.08,False)
	print([joint_values[0][0],joint_values[1][0],joint_values[2][0],joint_values[3][0],joint_values[4][0],joint_values[5][0]])

	
	print("Recording!")
	# get controller version
	con.get_controller_version()

	# setup recipes
	if not con.send_output_setup(output_names, output_types, frequency = frequency):
		logging.error('Unable to configure output')
		sys.exit()

	#start data synchronization
	if not con.send_start():
		logging.error('Unable to start synchronization')
		sys.exit()

	writeModes = 'wb' if binary else 'w'
	with open(output, writeModes) as csvfile:
		writer = None
		velocity = 0.001
		acceleration = 0.008
		dt = 0.01
		lookahead_time = 0.1
		gain = 300
			
				
			
			
		i = 1
		j =0
		keep_running = True
		while j < 5000:
			print(joint_values)
			print("Replay Started")
			start = time.time()
			rtde_c.servoJ([joint_values[0][j],joint_values[1][j],joint_values[2][j],joint_values[3][j],joint_values[4][j],joint_values[5][j]],velocity,acceleration,dt,lookahead_time, gain)    
			end = time.time()
			duration = end - start
			if duration < dt:
				time.sleep(dt - duration)
			rtde_c.servoStop()
			rtde_c.stopScript()
			j = j+1
		
		if binary:
			writer = csv_binary_writer.CSVBinaryWriter(csvfile, output_names, output_types)
		else:
			writer = csv_writer.CSVWriter(csvfile, output_names, output_types)
		
		writer.writeheader()

				
					
			
		try:
			state = con.receive(binary)
			if state is not None:
				writer.writerow(state)
				i += 1

		except KeyboardInterrupt:
			keep_running = False
		except rtde.RTDEException:
			con.disconnect()
			sys.exit()
			

		sys.stdout.write("\rComplete!\n")
		con.send_pause()
		con.disconnect()
	#Record('robot_data_replay.csv')
	
	print("Replay done!")
	    

def Plot():
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
	fig.write_html("Record_replay.html")


def Record(filename):

	print("Recording!")
	#parameters
	#parser = argparse.ArgumentParser()
	#parser.add_argument('--host', default='127.0.0.1', help='name of host to connect to (localhost)')
	#parser.add_argument('--port', type=int, default=30004, help='port number (30004)')
	#parser.add_argument('--samples', type=int, default=0, help='number of samples to record')
	#parser.add_argument('--frequency', type=int, default=125, help='the sampling frequency in Herz')
	#parser.add_argument('--config', default='/home/uthira/rtde-2.4.8/examples/record_configuration.xml', help='data configuration file to use (record_configuration.xml)')
	#parser.add_argument('--output', default='robot_data.csv', help='data output file to write to (robot_data.csv)')
	#parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
	#parser.add_argument("--binary", help="save the data in binary format", action="store_true")
	#args = parser.parse_args()
	host ='127.0.0.1'
	port =30004
	samples =5000
	frequency =125
	config = '/home/uthira/rtde-2.4.8/examples/record_configuration.xml'
	output =filename
	verbose = False
	binary = False
	if verbose:
		logging.basicConfig(level=logging.INFO)

	conf = rtde_config.ConfigFile(config)
	output_names, output_types = conf.get_recipe('out')

	con = rtde.RTDE(host, port)
	con.connect()

	# get controller version
	con.get_controller_version()

	# setup recipes
	if not con.send_output_setup(output_names, output_types, frequency = frequency):
		logging.error('Unable to configure output')
		sys.exit()

	#start data synchronization
	if not con.send_start():
		logging.error('Unable to start synchronization')
		sys.exit()

	writeModes = 'wb' if binary else 'w'
	with open(output, writeModes) as csvfile:
		writer = None

		if binary:
			writer = csv_binary_writer.CSVBinaryWriter(csvfile, output_names, output_types)
		else:
			writer = csv_writer.CSVWriter(csvfile, output_names, output_types)

		writer.writeheader()
	    
		i = 1
		keep_running = True
		while keep_running:
		
			if i%frequency == 0:
				if samples > 0:
					sys.stdout.write("\r")
					sys.stdout.write("{:.2%} done.".format(float(i)/float(samples))) 
					sys.stdout.flush()
				else:
					sys.stdout.write("\r")
					sys.stdout.write("{:3d} samples.".format(i)) 
					sys.stdout.flush()
			if samples > 0 and i >= samples:
				keep_running = False
			try:
				state = con.receive(binary)
				if state is not None:
					writer.writerow(state)
					i += 1

			except KeyboardInterrupt:
				keep_running = False
			except rtde.RTDEException:
				con.disconnect()
				sys.exit()
		

	sys.stdout.write("\rComplete!\n")
	con.send_pause()
	con.disconnect()

	


def main():
	try:
		while(1):
			print("1-Recording,2-Replaying,3-Plot,4-Home") 
			val = input("Enter your value: ") 						
			if(val== "1"):
				rtde_c.teachMode()
				print("..")
				Record('robot_data_record.csv')	
				rtde_c.endTeachMode()
				print('Done with Recording!')
							
			elif(val == "2"):
				Replay()			
				
						
			elif(val == "3"):			
				Plot()				
						
			elif(val == "4"):			
				Home()
					
					
			rtde_c.disconnect()
	except KeyboardInterrupt:
		rtde_c.disconnect()	
main()
