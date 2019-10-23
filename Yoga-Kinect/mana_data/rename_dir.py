

import os

#directory to be modified accordingly
root_direc = "/mnt/project2/home/kunals/Kinect_Yoga_data2/Raw_Data/Camera_1_Raw_data/"
folder = raw_input("Please enter folder name:")
direc = root_direc + folder + "/"

array = ['Padahastasana','TriyakTadasana','Katichakrasana','Tadasana','Ardhachakrasana','Virabhadrasana','Pranamasana','Vrikshasana','Natavarasana','Garudasana','Natarajasana','Tuladandasana']
array = array + ['Utkatasana','Trikonasana','ParivrittaTrikonasana','Gorakshasana','Santolanasana','Naukasana']


k = sum(os.path.isdir(os.path.join(direc,i)) for i in os.listdir(direc))
print(k)

if(k==18):
    j = 0
    for file in os.listdir(direc):
        print(file)
        os.rename(os.path.join(direc,file),os.path.join(direc,folder+'_'+array[j]))
        j = j+1
        print("yo")
if(k==19):
    array = array + ['Still']
    j = 0
    for file in os.listdir(direc):

        print(file)
        os.rename(os.path.join(direc,file),os.path.join(direc,folder+'_'+array[j]))
        j = j+1
        print("yo")

else:
    print("Please check file contents, there may be some extra files")
