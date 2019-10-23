# Kinect Yoga Recording Application

This is a program (version2.py) that allows you to record different Yoga postures, with the help of Microsoft Kinect V2. Each recording is saved in a folder named with the time of creation and in that folder the following data gets saved:
* color.avi - The rgb video of the recording
* depth.avi - The depth video feed from the kinect
* joints.csv - The skeletal joint coordinates that are detected by the kinect (Microsoft API) according to the following format:
            person, timestamp, joint_type, tracked/inferred, frame_number, x_coordinate (image space 1920x1080), y_coordinate (image space), joint_position_x (units?), joint_position_y (units?), joint_position_z (units?), joint_orientation_x (radians), joint_orientation_y (radians), joint_orientation_z (radians), joint_orientation_w
* color_timestamps.csv - Timestamps of every frame in the rgb video
* depth_timestamps.csv - Timestamps of every frame in the depth video

## Prerequisites

This only works on a Windows machine, because the Microsoft Kinect SDK is only available for the Windows

* Microsoft Kinect SDK
* Windows 8 or higher
* Python 3

There are several python library dependencies for the program:

* PyKinect2
* OpenCV 3
* Pygame

Please visit https://github.com/Kinect/PyKinect2 for more dependencies.

## Conversion to an Application

If you want to deploy the program as an executable application that can be directly downloaded by anyone and used, follow these instuction:

* Successfully run the program in an operating system for which you want to create the executable application.
* Install PyInstaller (pip install pyinstaller)
* Run 'pyinstaller version2.py' to generate the executable. Refer to http://www.pyinstaller.org/
