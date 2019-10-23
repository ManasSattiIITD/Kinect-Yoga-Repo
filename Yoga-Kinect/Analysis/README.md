# Skeletal Joints Analysis from the Microsoft Kinect

* skeleton.py - program for generating videos and joint smoothing
* align.py - align one yoga exercise to another master/reference frame
* Segment/segment.py - segment the start and end of posture
* Segment/posture_data.py - print data about the posture

Further help can be seen using the "--help" flag of each application. 

## Prerequisites

The code runs with Python 3, so make sure you have latest version installed before testing. This program has several python library dependencies, most important of which are:

* OpenCV 3 with ffmpeg
* Matplotlib 
* NumPy
* Scipy

## Conversion to an Application

If you want to deploy the program as an executable application that can be directly downloaded by anyone and used, follow these instuction:

* Successfully run the program in an operating system for which you want to create the executable application.
* Install PyInstaller (pip install pyinstaller)
* Run 'pyinstaller version2.py' to generate the executable. Refer to http://www.pyinstaller.org/


## Files added by Adhish (WIP)

* First, ensure that the names of all the folders inside the dataset are 
standardized, for this, use minor_changes and rename_pebl_csv
* To get final corelations, first run stability1 which will 
generate OUTPUT.csv containing stability values. Then run extract_pebl, 
to append pebl metric values to OUTPUT.csv, then run obtain_correlation_matrix.py

* stability -- To calculate stability of one subject one asan (generic script)
* stability1 -- Iterative version that runs over all subjects and asanas (in the current structure). It wil generate OUTPUT.csv containing stability values. 
* minor_changes -- To standardize asan names in the directory structure and file names (there are spelling mistakes in general). May need to run more than once.
* generates_cmp -- Generates correlation matix with p-values (incomplete and inefficient -- need to run for 1 week on cerebrum to generate numbers for 10K iterations. For specific matrcies it gives errors in p-values).
* obtain_correlation_matrix.py -- Used to obtain correlation matrix from OUTPUT.csv (currently not well structured. OUTPUT.csv must be in the same folder).
* classifications.py -- Package that classifies the asanas (horizontal, vertical etc.). Used by stability1
* extract_pebl -- Extraction of PEBL metrics. Need to run it once for each test.
* rename_pebl_csv -- To rename csv's kept inside folders of every subject. The CSV name needs to match the subject name.
* rename_stab -- (Obsolete now) To change name_asana to subjectID_asana in the data (and inside every file's name changed).
* simon.py -- (Obsolete now). To process Simon task. Use the simon in extract_pebl -- it has more metrics.
* skeletons1.py -- (Not working. Might need some package installations in python3) Iterative version of skeletons.py to generate videos of all the asanas and all the subjects.



