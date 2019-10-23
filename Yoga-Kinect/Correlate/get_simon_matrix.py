
# coding: utf-8

# In[42]:


import csv
import numpy as np
import sys
import os
#arguements: <aasana file>


# In[43]:


aasana = sys.argv[1]+'.csv'
#aasana = 'Tadasana.csv'


# In[44]:


aasana_data = []
headings = []
with open(aasana,'r') as data:
    csv_reader = csv.reader(data)
    i = 0
    for row in csv_reader:
        if(i==0):
            headings = row
        elif(i%2==0):
            aasana_data.append(row)
        i = i+1


# In[46]:


colwise = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
for row in aasana_data:
    for i in range(len(row)):
        colwise[i].append(row[i])


# In[47]:


for i in range(1,15):
    colwise[i] = np.float64(colwise[i])


# In[49]:


x = []
corrcoef = []
for i in range(2,len(headings)):
    X = np.float64(colwise[1])
    Y = np.float64(colwise[i])
    meanX = np.mean(X)
    meanY = np.mean(Y)
    X_neg = X-meanX
    Y_neg = Y-meanY
    temp = X_neg*Y_neg
    covXY = np.mean(temp)
    sigmaX = np.std(X)
    sigmaY = np.std(Y)
    corr = covXY/(sigmaX*sigmaY)
    corrcoef.append(corr)
    #print(meanX,meanY,X_neg)


# In[55]:


corrcoef,len(corrcoef)


# In[67]:


snowball = []

with open('corrcoeff.csv','w+') as check:
    csv_reader = csv.reader(check)
    for row in csv_reader:
        #first_row = row0
        snowball.append(1)
        print('ysy')
        
with open('corrcoeff.csv','a+') as file:
    csv_writer = csv.writer(file)
    if( len(snowball)==0):
        fRow = ['Aasana Name']
        for title in headings[2:len(headings)]:
            fRow.append(title)
        csv_writer.writerow(fRow)
    
    row = [aasana.split('.')[0]]
    for i in corrcoef:
        row.append(i)
    csv_writer.writerow(row)


# In[51]:




