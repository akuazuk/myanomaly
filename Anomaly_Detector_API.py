#!/usr/bin/env python
# coding: utf-8

# # Anomaly Detector API

# In[18]:


# To start sending requests to the Anomaly Detector API, paste your Anomaly Detector resource access key below,
# and replace the endpoint variable with the endpoint for your region or your on-premise container endpoint. 
# Endpoint examples:
# https://westus2.api.cognitive.microsoft.com/anomalydetector/v1.0/timeseries/entire/detect
# http://127.0.0.1:5000/anomalydetector/v1.0/timeseries/entire/detect
#apikey = '' 
#endpoint = ''
apikey = '' 
endpoint = ''


# In[19]:


import requests
import json
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Import library to display results
import matplotlib.pyplot as plt
#get_ipython().run_line_magic('matplotlib', 'inline')


# In[20]:


from bokeh.plotting import figure,output_notebook, show
from bokeh.palettes import Blues4
from bokeh.models import ColumnDataSource,Slider
import datetime
from bokeh.io import push_notebook
from dateutil import parser
from ipywidgets import interact, widgets, fixed
#output_notebook()


# In[21]:


def detect(endpoint, apikey, request_data):
    headers = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': apikey}
    response = requests.post(endpoint, data=json.dumps(request_data), headers=headers)
    if response.status_code == 200:
        return json.loads(response.content.decode("utf-8"))
    else:
        print(response.status_code)
        raise Exception(response.text)


# In[22]:


def build_figure(sample_data, sensitivity):
    sample_data['sensitivity'] = sensitivity
    result = detect(endpoint, apikey, sample_data)
    columns = {'expectedValues': result['expectedValues'], 'isAnomaly': result['isAnomaly'], 'isNegativeAnomaly': result['isNegativeAnomaly'],
          'isPositiveAnomaly': result['isPositiveAnomaly'], 'upperMargins': result['upperMargins'], 'lowerMargins': result['lowerMargins'],
          'timestamp': [parser.parse(x['timestamp']) for x in sample_data['series']], 
          'value': [x['value'] for x in sample_data['series']]}
    response = pd.DataFrame(data=columns)
    values = response['value']
    label = response['timestamp']
    anomalies = []
    anomaly_labels = []
    index = 0
    anomaly_indexes = []
    p = figure(x_axis_type='datetime', title="AI Anomaly Detection in data ({0} Sensitvity)".format(sensitivity), width=800, height=600)
    for anom in response['isAnomaly']:
        if anom == True and (values[index] > response.iloc[index]['expectedValues'] + response.iloc[index]['upperMargins'] or 
                         values[index] < response.iloc[index]['expectedValues'] - response.iloc[index]['lowerMargins']):
            anomalies.append(values[index])
            anomaly_labels.append(label[index])
            anomaly_indexes.append(index)
        index = index+1
    upperband = response['expectedValues'] + response['upperMargins']
    lowerband = response['expectedValues'] -response['lowerMargins']
    band_x = np.append(label, label[::-1])
    band_y = np.append(lowerband, upperband[::-1])
    boundary = p.patch(band_x, band_y, color=Blues4[2], fill_alpha=0.5, line_width=1, legend_label='Boundary')
    p.line(label, values, legend_label='Value', color="#2222aa", line_width=1)
    p.line(label, response['expectedValues'], legend_label='ExpectedValue',  line_width=1, line_dash="dotdash", line_color='olivedrab')
    anom_source = ColumnDataSource(dict(x=anomaly_labels, y=anomalies))
    anoms = p.circle('x', 'y', size=5, color='tomato', source=anom_source)
    p.legend.border_line_width = 1
    p.legend.background_fill_alpha  = 0.1
    show(p, notebook_handle=True)


# In[23]:


from finanomaly import Anomaly
company = ["DJI", "AAPL", "NFLX", "NFLX2", "META", "GOOG", "AMZN", "SP500", "NASDAQ"]
fin_files = Anomaly(company)
fin_files.stock()


# ## Vizualizing anomalies throughout your data
# 

# In[24]:


#daily sample
sample_data = json.load(open('GOOG.json'))
sample_data['period'] = 168
sample_data['granularity'] = 'daily'
# 95 sensitivity
build_figure(sample_data,95)


# In[25]:


#daily sample
sample_data = json.load(open('META.json'))
sample_data['period'] = 168
sample_data['granularity'] = 'daily'
# 95 sensitivity
build_figure(sample_data,95)


# In[26]:


#daily sample
sample_data = json.load(open('AMZN.json'))
sample_data['period'] = 168
sample_data['granularity'] = 'daily'
# 95 sensitivity
build_figure(sample_data,95)


# In[27]:


#daily sample
sample_data = json.load(open('NFLX.json'))
sample_data['period'] = 168
sample_data['granularity'] = 'daily'
# 95 sensitivity
build_figure(sample_data,95)


# In[28]:


#daily sample
sample_data = json.load(open('NFLX2.json'))
sample_data['period'] = 168
sample_data['granularity'] = 'daily'
# 95 sensitivity
build_figure(sample_data,95)


# In[29]:


#daily sample
sample_data = json.load(open('AAPL.json'))
sample_data['period'] = 168
sample_data['granularity'] = 'daily'
# 95 sensitivity
build_figure(sample_data,95)


# In[30]:


#daily sample
sample_data = json.load(open('SP500.json'))
sample_data['period'] = 168
sample_data['granularity'] = 'daily'
# 95 sensitivity
build_figure(sample_data,95)


# In[31]:


#daily sample
sample_data = json.load(open('NASDAQ.json'))
sample_data['period'] = 168
sample_data['granularity'] = 'daily'
# 95 sensitivity
build_figure(sample_data,95)


# In[36]:


#daily sample
sample_data = json.load(open('DJI.json'))
sample_data['period'] = 168
sample_data['granularity'] = 'daily'
# 95 sensitivity
build_figure(sample_data,95)


# In[33]:


#daily sample
#sample_data = json.load(open('rentApt.json'))
#sample_data['period'] = 24
#sample_data['granularity'] = 'monthly'
#sample_data['customInterval'] = 7
# 95 sensitivity
#build_figure(sample_data,90)


# In[35]:


#daily sample
#sample_data = json.load(open('car5.json'))
#sample_data['period'] = 96
#sample_data['granularity'] = 'weekly'
# 95 sensitivity
#build_figure(sample_data,90)


# In[ ]:




