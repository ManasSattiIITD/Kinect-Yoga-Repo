#!/usr/bin/env python
# coding: utf-8

# In[1]:


# csv standardization
import os
import sys


# In[2]:


if(len(sys.argv) != 3):
    sys.exit('Usage: <directory of organised data pebl data> <userID>\nChanges the name of the csv according to the subject ID')


# In[19]:


directory = sys.argv[1]
userID = sys.argv[2]
# directory = '.'
# userID = '1'
try:
    os.chdir(directory+'/'+userID)
except:
    sys.exit('no such file or directory')


# In[12]:


list_of_csv = next(os.walk(os.getcwd()))[2]
#if(len(list_of_csv)!=1):
#    sys.exit('wrong directory')

j = 0
for i in range(len(list_of_csv)):
	j = 0
	split_name = list_of_csv[i].split('.')
	# check if this name is a csv file
	if(split_name[len(split_name)-1]=='csv'):
		j = i
		subnames = list_of_csv[j].split('-')
		number_of_subnames = len(subnames)
		new_name = ''

		for i in range(len(subnames)-1):
			new_name = new_name + subnames[i] + '-'
		new_name = new_name + userID +'.csv'
		os.rename(list_of_csv[j],new_name)
		print(os.getcwd(),new_name)

