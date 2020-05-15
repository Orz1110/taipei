import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

filepath = "/content/drive/My Drive/VD/"
filename = os.listdir(filepath)
# filename
# for i in range(len(filename)):
data_VD_all = pd.DataFrame([])

for i in range(len(filename)):
  data_VD = pd.read_csv(filepath+filename[i])
  data_VD = data_VD[data_VD["DEVICEID"]=="V0130A0"]
  data_VD_all = pd.concat([data_VD, data_VD_all])
  print(data_VD_all)
data_VD_all = data_VD_all[data_VD_all["DEVICEID"]=="V0130A0"]
data = data_VD_all[['BIGVOLUME','CARVOLUME','MOTORVOLUME']]


import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Box(name = 'BIGVOLUME' ,y=data['BIGVOLUME'].values))
fig.add_trace(go.Box(name = 'CARVOLUME' ,y=data['CARVOLUME'].values))
fig.add_trace(go.Box(name = 'MOTORVOLUME' ,y=data['MOTORVOLUME'].values))

fig.show()