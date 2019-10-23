# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 19:12:57 2019

@author: admin
"""

import argparse
import sys
import os
import shutil

srcfile = 'E:\\Yoga-Kinect\\Analysis\\openh264-1.8.0-win64.dll'
fname = 'openh264-1.8.0-win64.dll'

directory = sys.argv[1] # directory containing all subject names
os.chdir(directory)
list_of_subjects = next(os.walk(os.getcwd()))[1]
for subject in list_of_subjects:
    os.chdir(subject)
    list_of_aasanas = next(os.walk(os.getcwd()))[1]
    for aasana in list_of_aasanas:
        os.chdir(aasana)
        #dstdir =  os.path.join(aasana, os.path.dirname(fname))
        shutil.copy(srcfile, fname)
        os.chdir('..')
    os.chdir('..')
