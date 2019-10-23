#!/usr/bin/env python

# coding: utf-8

# In[1]:


import os
import sys
import numpy as np
import csv

def usage():
	print('Usage\nInput arguments "0" for a detailed correlation matrix, "1" for a condensed correlation matrix ')
	sys.exit()
    #pass

if(len(sys.argv)!=2):
	usage()
    
# create a dict of all metrics
all_metrics = {}
# create a list of keys
names_of_all_metrics = []

subjIDs = []


with open ('OUTPUT.csv','r') as output:
    csv_reader = csv.reader(output)
    i = 0
    # inititalize metric name
    metric_name = ''
    # initialize the key name
    subjID = ''
    # read the csv and classify
    for row in csv_reader:
        if(not row):
            print(True)
            continue
        i = i + 1
        
        # check if row represents an aasana or pebl data
        if(int(sys.argv[1])==1):
        	components = row[2].split('_')
        	if(components[0] == 'JointType'):
        		continue
        # extract metric value
        try:
            value = np.float64(row[3])
        except:
            #print('restarting loop')
            continue
        metric_name = row[1]+'_'+row[2]
        # add subjID to the list of keys of inner dict
        subjID = row[0]
        if(subjID not in subjIDs):
            subjIDs.append(subjID)
        
        if (metric_name not in names_of_all_metrics):
            names_of_all_metrics.append(metric_name)
            all_metrics[metric_name] = {}  
        inner_dict = all_metrics[metric_name]
        inner_dict[subjID] = value
# In[9]:

# generates a row containing a list of metrics and
# writes it to the csv as heading
# if such a csv already exists, its content is erased
file_name = 'CORRELATION_MATRIX.csv'
if(int(sys.argv[1])==1):
	file_name = 'CONDENSED_CORRELATION_MATRIX.csv'
with open(file_name,'w') as corrM:
    csv_writer = csv.writer(corrM)
    row = ['Metric']
    for any_metric in names_of_all_metrics:
        row.append(any_metric)
    csv_writer.writerow(row)


# In[10]:


prProg = 0

for first_metric in names_of_all_metrics:
    # user updates
    print('processing correlation '+ str(prProg+1) +' out of '+ str(len(names_of_all_metrics)))
    prProg += 1
    # extract inner dict for the given metric
    first_data = all_metrics[first_metric]
    # initialize the row to be printed
    row = [first_metric]
    for second_metric in names_of_all_metrics:
        corr_first = []
        corr_second = []
        # obtain inner dict to correlate
        second_data = all_metrics[second_metric]
        #print(second_data)
        for subjID in subjIDs:
            try:
                #print(first_data[subjID],second_data[subjID])
                metric1_value = first_data[subjID]
                
                metric2_value = second_data[subjID]
                
                #print('|||'+metric1_value,metric2_value)
                corr_first.append(np.float64(metric1_value))
                corr_second.append(np.float64(metric2_value))
                continue
            except:
                #print('Bartleby '+subjID)
                continue
        # obtain correlation
        # print(corr_first)
        # print(corr_second)
        
        X = np.array(corr_first,dtype = np.float64)
        Y = np.array(corr_second,dtype = np.float64 )
        #print(1)
        sigmaX = np.std(X)
        sigmaY = np.std(Y)
        #print(2)
        meanX = np.mean(X)
        meanY = np.mean(Y)
        #print(3)
        tempX = X-np.mean(X)
        tempY = Y-np.mean(Y)
        #print(4)
        temp = tempX*tempY
        covXY = np.mean(temp)
        corrXY = covXY/(sigmaX*sigmaY)
        row.append(corrXY)
        #print(5)
        # print(corrXY)
        # if the correlation cannot be obtained, append a string instead of the correlation value
        #except:
            #print(Exception)
            # print(corr_first,corr_second)
        #    row.append('correlation error')
    with open(file_name,'a') as corrM:
        #print(file_name, row)
        csv_writer = csv.writer(corrM)
        csv_writer.writerow(row)
        # user updates
        print('fin: '+str(prProg))

