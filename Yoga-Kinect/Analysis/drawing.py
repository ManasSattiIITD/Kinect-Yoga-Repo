import cv2
import numpy as np

FRAME_DIMS = (1080,1920,3)

def drawline(frame, list, joint1, joint2, color_inferred, color_tracked):
    #if(float(list[joint1][5])>1400 or float(list[joint1][6])>1000 or float(list[joint2][5])>1400 or float(list[joint2][6])>1000 or ):
    #        return
        
    a = float(list[joint1][5])
    b = float(list[joint1][6])
    c = float(list[joint2][5])
    d = float(list[joint2][6])
    if(a==float('inf') or b==float('inf') or c==float('inf') or d==float('inf') or a==float('-inf') or b==float('-inf') or c==float('-inf') or d==float('-inf')):
        return
    
    if(list[joint1][3]=='inferred' or list[joint2][3]=='inferred'):
        frame = cv2.line(frame, (round(a),round(b)),(round(c),round(d)),color_inferred,2)
    else:
        frame = cv2.line(frame, (round(a),round(b)),(round(c),round(d)),color_tracked,2)


def drawframe(list, color_inferred, color_tracked):
    frame = np.zeros(FRAME_DIMS,dtype=np.uint8)

    #lines
    if('JointType_Head' in list and 'JointType_Neck' in list):
        drawline(frame, list, 'JointType_Head', 'JointType_Neck', color_inferred, color_tracked)
    if('JointType_Neck' in list and 'JointType_SpineShoulder' in list):
        drawline(frame, list, 'JointType_SpineShoulder', 'JointType_Neck', color_inferred, color_tracked)
    if('JointType_SpineShoulder' in list and 'JointType_SpineMid' in list):
        drawline(frame, list, 'JointType_SpineShoulder', 'JointType_SpineMid', color_inferred, color_tracked)
    if('JointType_SpineMid' in list and 'JointType_SpineBase' in list):
        drawline(frame, list, 'JointType_SpineMid', 'JointType_SpineBase', color_inferred, color_tracked)
    if('JointType_SpineShoulder' in list and 'JointType_ShoulderRight' in list):
        drawline(frame, list, 'JointType_SpineShoulder', 'JointType_ShoulderRight', color_inferred, color_tracked)
    if('JointType_SpineShoulder' in list and 'JointType_ShoulderLeft' in list):
        drawline(frame, list, 'JointType_SpineShoulder', 'JointType_ShoulderLeft', color_inferred, color_tracked)
    if('JointType_SpineBase' in list and 'JointType_HipRight' in list):
        drawline(frame, list, 'JointType_SpineBase', 'JointType_HipRight', color_inferred, color_tracked)
    if('JointType_SpineBase' in list and 'JointType_HipLeft' in list):
        drawline(frame, list, 'JointType_SpineBase', 'JointType_HipLeft', color_inferred, color_tracked)

    # Right Arm
    if('JointType_ShoulderRight' in list and 'JointType_ElbowRight' in list):
        drawline(frame, list, 'JointType_ShoulderRight', 'JointType_ElbowRight', color_inferred, color_tracked)
    if('JointType_ElbowRight' in list and 'JointType_WristRight' in list):
        drawline(frame, list, 'JointType_ElbowRight', 'JointType_WristRight', color_inferred, color_tracked)
    if('JointType_WristRight' in list and 'JointType_HandRight' in list):
        drawline(frame, list, 'JointType_WristRight', 'JointType_HandRight', color_inferred, color_tracked)
    if('JointType_HandRight' in list and 'JointType_HandTipRight' in list):
        drawline(frame, list, 'JointType_HandRight', 'JointType_HandTipRight', color_inferred, color_tracked)
    if('JointType_WristRight' in list and 'JointType_ThumbRight' in list):
        drawline(frame, list, 'JointType_WristRight', 'JointType_ThumbRight', color_inferred, color_tracked)

    # Left Arm
    if('JointType_ShoulderLeft' in list and 'JointType_ElbowLeft' in list):
        drawline(frame, list, 'JointType_ShoulderLeft', 'JointType_ElbowLeft', color_inferred, color_tracked)
    if('JointType_ElbowLeft' in list and 'JointType_WristLeft' in list):
        drawline(frame, list, 'JointType_ElbowLeft', 'JointType_WristLeft', color_inferred, color_tracked)
    if('JointType_WristLeft' in list and 'JointType_HandLeft' in list):
        drawline(frame, list, 'JointType_WristLeft', 'JointType_HandLeft', color_inferred, color_tracked)
    if('JointType_HandLeft' in list and 'JointType_HandTipLeft' in list):
        drawline(frame, list, 'JointType_HandLeft', 'JointType_HandTipLeft', color_inferred, color_tracked)
    if('JointType_WristLeft' in list and 'JointType_ThumbLeft' in list):
        drawline(frame, list, 'JointType_WristLeft', 'JointType_ThumbLeft', color_inferred, color_tracked)

    # Right Leg
    if('JointType_HipRight' in list and 'JointType_KneeRight' in list):
        drawline(frame, list, 'JointType_HipRight', 'JointType_KneeRight', color_inferred, color_tracked)
    if('JointType_KneeRight' in list and 'JointType_AnkleRight' in list):
        drawline(frame, list, 'JointType_KneeRight', 'JointType_AnkleRight', color_inferred, color_tracked)
    if('JointType_AnkleRight' in list and 'JointType_FootRight' in list):
        drawline(frame, list, 'JointType_AnkleRight', 'JointType_FootRight', color_inferred, color_tracked)

    # Left Leg
    if('JointType_HipLeft' in list and 'JointType_KneeLeft' in list):
        drawline(frame, list, 'JointType_HipLeft', 'JointType_KneeLeft', color_inferred, color_tracked)
    if('JointType_KneeLeft' in list and 'JointType_AnkleLeft' in list):
        drawline(frame, list, 'JointType_KneeLeft', 'JointType_AnkleLeft', color_inferred, color_tracked)
    if('JointType_AnkleLeft' in list and 'JointType_FootLeft' in list):
        drawline(frame, list, 'JointType_AnkleLeft', 'JointType_FootLeft', color_inferred, color_tracked)

    #circles
    for _, item in list.items():
        cval = max(255, 0)
        rad = max(5, 0)
        #print(item)
        #print(color[item[2]])
        a = float(item[5])
        b = float(item[6])
        #print("a: ",a)
        #print("b: ",b)
                
        if(a==float('inf')or b==float('inf') or a==float('-inf')or b==float('-inf')):
            print (item[2],"out of frame at ",item[1])
            continue
        frame = cv2.circle(frame, (round(a),round(b)), round(rad), (cval,cval,cval), -1)

    return frame

