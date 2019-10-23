
# coding: utf-8

# In[1]:


import csv
import os
import sys
import numpy as np
# input arguements <filename> <subjectid> <aasanid>


# In[2]:


filename = sys.argv[1]
#filename = 'version2\simon\simon\data\Pranjual\simon-Pranjual.csv'


# In[3]:


dataset = []
with open(filename,'r+') as sim:
    csv_reader = csv.reader(sim)
    for row in csv_reader:
        dataset.append(row)


# In[5]:


three = [[],[],[],[],[],[]] #1p 2p 1n 2n 1z 2z
for row in dataset[4:len(dataset)]:
    if (row[2] == '1' and np.float64(row[3])>0) :
        three[0].append(row)
    elif (row[2] == '2' and np.float64(row[3])>0) :
        three[1].append(row)
    elif row[2] == '1' and np.float64(row[3])<0 :
        three[2].append(row)
    elif row[2] == '2' and np.float64(row[3])<0 :
        three[3].append(row)
    elif row[2] == '1' and np.float64(row[3])==0 :
        three[4].append(row)
    elif row[2] == '2' and np.float64(row[3])==0 :
        three[5].append(row)
    else:
        print('__')


# In[6]:


reaction_time = [[],[],[],[],[],[]]
means = [[],[],[],[],[],[],[]]
variances = [[],[],[],[],[],[]]
for i in range(len(three)):
    for row in three[i]:
        reaction_time[i].append(np.float64(row[7]))
    means[i]=(np.mean(reaction_time[i]))
    variances[i]=(np.var(reaction_time[i]))
means[6] = np.mean(means[0:5])


# In[8]:


try:
    os.chdir('simon_correlation')
except:
    os.mkdir('simon_correlation')
    os.chdir('simon_correlation')


# In[27]:


new_rows = [['name','joint_stability_variance',
             'mean(1p)','mean(2p)','mean(1n)','mean(2n)','mean(1z)','mean(2z)','mean',
            'var(1p)','var(2p)','var(1n)','var(2n)','var(1z)','var(2z)']]
name = sys.argv[2]
aasan = sys.argv[3]
#name = 'Kunal'
#aasan = 'Natvarasana'
with open(aasan+'.csv','r') as findname:
    csv_reader = csv.reader(findname)
    flag = False
    for row1 in csv_reader:
        
        try:
            row = []
            row.append(row1[0])
            row.append(row1[1])
            if row[0] == new_rows[0][0]:
                continue
            if row[0] == name:
                flag = True
                for mean in means:
                    row.append(mean)
                for var in variances:
                    row.append(var)
                new_rows.append(row)
            else:
                new_rows.append(row1)
        except:
            continue
    if flag == False :
        row1 = [name,0]
        for mean in means:
            row1.append(mean)
        for var in variances:
            row1.append(var)
        new_rows.append(row1)


# In[28]:


with open(aasan+'.csv','w') as fileWrite:
    writer = csv.writer(fileWrite)
    for row in new_rows:
        writer.writerow(row)


# In[13]:




