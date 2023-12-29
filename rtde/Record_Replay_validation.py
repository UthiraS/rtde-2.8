#!/usr/bin/env python
# coding: utf-8



import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import sys
import rtde.csv_reader as csv_reader
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



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
fig.write_html("Record_replay.html")





