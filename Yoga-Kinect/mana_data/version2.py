from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import numpy as np
from threading import Thread

import time
import cv2
import sys, os
from datetime import datetime
import time
import csv
import ctypes
import _ctypes
import pygame
import keyboard
import sys
import pyaudio
import wave

if sys.hexversion >= 0x03000000:
    import _thread as thread
else:
    import thread
# initialize userID and aasanaID
subjID = ''
aasanaID = ''
# colors for drawing different bodies
SKELETON_COLORS = [pygame.color.THECOLORS["red"],
                   pygame.color.THECOLORS["blue"],
                   pygame.color.THECOLORS["green"],
                   pygame.color.THECOLORS["orange"],
                   pygame.color.THECOLORS["purple"],
                   pygame.color.THECOLORS["yellow"],
                   pygame.color.THECOLORS["violet"]]

joint_types = ['JointType_SpineBase',
               'JointType_SpineMid',
               'JointType_Neck',
               'JointType_Head',
               'JointType_ShoulderLeft',
               'JointType_ElbowLeft',
               'JointType_WristLeft',
               'JointType_HandLeft',
               'JointType_ShoulderRight',
               'JointType_ElbowRight',
               'JointType_WristRight',
               'JointType_HandRight',
               'JointType_HipLeft',
               'JointType_KneeLeft',
               'JointType_AnkleLeft',
               'JointType_FootLeft',
               'JointType_HipRight',
               'JointType_KneeRight',
               'JointType_AnkleRight',
               'JointType_FootRight',
               'JointType_SpineShoulder',
               'JointType_HandTipLeft',
               'JointType_ThumbLeft',
               'JointType_HandTipRight',
               'JointType_ThumbRight'
               ]


class BodyGameRuntime(object):
    def __init__(self):
        pygame.init()

        # Set the width and height of the screen [width, height]
        self._infoObject = pygame.display.Info()
        self._screen = pygame.display.set_mode((self._infoObject.current_w >> 1, self._infoObject.current_h >> 1),
                                               pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE, 32)

        pygame.display.set_caption("Kinect for Windows v2 Body Game")

        # Loop until the user clicks the close button.
        self._done = False

        self.now = 0

        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Kinect runtime object, we want only color and body frames
        self._kinect = PyKinectRuntime.PyKinectRuntime(
            PyKinectV2.FrameSourceTypes_Color |  PyKinectV2.FrameSourceTypes_Infrared | PyKinectV2.FrameSourceTypes_Body |
            PyKinectV2.FrameSourceTypes_Depth)

        # back buffer surface for getting Kinect color frames, 32bit color, width and height equal to the Kinect color frame size
        self._frame_surface = pygame.Surface(
            (self._kinect.color_frame_desc.Width, self._kinect.color_frame_desc.Height), 0, 32)

        self.frames = np.zeros((100,self._kinect.color_frame_desc.Height, self._kinect.color_frame_desc.Width,3), dtype=np.uint8)

        # here we will store skeleton data
        self._bodies = None

        self._joints_with_time = None
        self.path = None
        self._key_press = None
        self._key_press_rec = []
        self._key_press_rec_iter= 0
        self._key_press_rec_label = ['Start time of asana',"Start time of asana's hold-time","End time of asana's hold-time","End time of asana"]
        # self._cnt = 0
        self._frameno = 0
        self.hot_keys = []
        self._video_frameno = None
        self._timestamps = None
        self._video_color = None
        self._video_depth = None
        self._video_infrared = None

        self._audio = None
        self.MOUSE_BUTTON_DOWN = 1
        self.MOUSE_BUTTON_UP = 0

        self.clicked = False
        self.prev_mouse_state = self.MOUSE_BUTTON_DOWN

        self.isRecording = False

        self.sound_thread = None
        self.ir_counter = 0
        self.depth_counter = 0
        self.audio_frames = []
        self.audio_stop_flag = False
        self.audio_is_stopped = False


    def csv_writer(self, filename, data):
        with open(filename, "a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for line in data:
                writer.writerow(line)

    def store_joints(self, joints, joint_orientations, jointPoints, person):
        for i in range(0, 25):
            joint = joints[i]
            joint_coord = jointPoints[i]
            orientation = joint_orientations[i].Orientation

            if (joint.TrackingState == 2):
                # print(i," is tracked.")
                self._joints_with_time.append(
                    [person, self.now, joint_types[i], 'tracked', self._frameno,
                    jointPoints[i].x, jointPoints[i].y,
                    joint.Position.x, joint.Position.y, joint.Position.z,
                    orientation.x, orientation.y, orientation.z, orientation.w])
            elif (joint.TrackingState == 1):
                # print(i," is inferred.")
                self._joints_with_time.append(
                    [person, self.now, joint_types[i], 'inferred', self._frameno,
                    jointPoints[i].x, jointPoints[i].y,
                    joint.Position.x, joint.Position.y, joint.Position.z,
                    orientation.x, orientation.y, orientation.z, orientation.w])

            if (len(self._joints_with_time) == 100):
                self.csv_writer(self.path + '/joints.csv', self._joints_with_time)
                self._joints_with_time = []

    def draw_body_bone(self, joints, jointPoints, color, joint0, joint1):
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;

        # both joints are not tracked
        if (joint0State == PyKinectV2.TrackingState_NotTracked) or (joint1State == PyKinectV2.TrackingState_NotTracked):
            return

        # both joints are not *really* tracked
        if (joint0State == PyKinectV2.TrackingState_Inferred) and (joint1State == PyKinectV2.TrackingState_Inferred):
            return

        # ok, at least one is good
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)

        # self.csv_writer([[joint0,jointPoints[joint0].x,jointPoints[joint0].y],[joint1,jointPoints[joint1].x,jointPoints[joint1].y]])

        try:
            pygame.draw.line(self._frame_surface, color, start, end, 8)
        except:  # need to catch it due to possible invalid positions (with inf)
            pass

    def draw_body(self, joints, jointPoints, color):
        # Torso
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Head, PyKinectV2.JointType_Neck);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Neck, PyKinectV2.JointType_SpineShoulder);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder,
                            PyKinectV2.JointType_SpineMid);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineMid, PyKinectV2.JointType_SpineBase);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder,
                            PyKinectV2.JointType_ShoulderRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder,
                            PyKinectV2.JointType_ShoulderLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipLeft);

        # Right Arm
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderRight,
                            PyKinectV2.JointType_ElbowRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowRight,
                            PyKinectV2.JointType_WristRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight,
                            PyKinectV2.JointType_HandRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandRight,
                            PyKinectV2.JointType_HandTipRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight,
                            PyKinectV2.JointType_ThumbRight);

        # Left Arm
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderLeft,
                            PyKinectV2.JointType_ElbowLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowLeft, PyKinectV2.JointType_WristLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_HandLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandLeft,
                            PyKinectV2.JointType_HandTipLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_ThumbLeft);

        # Right Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipRight, PyKinectV2.JointType_KneeRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeRight,
                            PyKinectV2.JointType_AnkleRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_AnkleRight,
                            PyKinectV2.JointType_FootRight);

        # Left Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipLeft, PyKinectV2.JointType_KneeLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeLeft, PyKinectV2.JointType_AnkleLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_AnkleLeft, PyKinectV2.JointType_FootLeft);

    def draw_color_frame(self, frame, target_surface):
        target_surface.lock()
        address = self._kinect.surface_as_array(target_surface.get_buffer())
        ctypes.memmove(address, frame.ctypes.data, frame.size)
        del address
        target_surface.unlock()

    def surface_to_string(self, surface):
        return pygame.image.tostring(surface, 'RGB')

    def write_key_press(self):
        self.csv_writer(self.path + '/key_press.csv', self._key_press)


    def write_key_press_rec(self):
        self.csv_writer(self.path + '/key_press_rec.csv', [["Label","Time elaspsed since start of recording(in sec) :-"]] + self._key_press_rec)







    def startRecording(self):

        def add_key_press_rec(time_data):
            if self._key_press_rec_iter >3:
                return
            else:
                self._key_press_rec_iter+=1
                self._key_press_rec.append([self._key_press_rec_label(self._key_press_rec_iter),time_data])

        def audio_record(path_of_audio):
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 2
            RATE = 44100
            # RECORD_SECONDS = 5
            WAVE_OUTPUT_FILENAME = path_of_audio
            p = pyaudio.PyAudio()

            stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)

            print("* initiating audio recording *")
            self.audio_is_stopped = False
            self.audio_frames = []

            while self.audio_stop_flag == False:
                data = stream.read(CHUNK)
                self.audio_frames.append(data)

            stream.stop_stream()
            stream.close()
            p.terminate()
            print("* done audio recording *")
            wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(self.audio_frames))
            wf.close()
            self.audio_is_stopped = True


        self._joints_with_time = []
        # self.path = str(datetime.now().date()) + ' at ' + str(datetime.now().hour) + '.' + str(
        #    datetime.now().minute) + '.' + str(datetime.now().second)
        # name of the directory will be saved as subjID_aasanaID
        subjID = input('enter subject ID: ')
        aasanaID = input('enter aasana name: ')
        self.path = subjID+'_'+aasanaID
        list_of_dir = next(os.walk(os.getcwd()))[1]
        if(self.path in list_of_dir):
            # if the directory already exists
            for i in range(10000):
                print('ALREADY EXISTS ..!!\n\nALREADY EXISTS ..!!\n\nALREADY EXISTS ..!!')
            self.path = None
            # flip it once
            self.isRecording = not self.isRecording
            self.clicked = not self.clicked
            return
        os.mkdir(self.path)
        self.ir_path = self.path+'/ir_files'
        self.depth_path = self.path+'/depth_files'
        os.mkdir(self.ir_path)
        os.mkdir(self.depth_path)

        # self._cnt = 0
        self._frameno = 0
        self._video_frameno = [0, 0, 0, 0]
        self._timestamps = [[], [], [], []]
        codec_x264 = cv2.VideoWriter_fourcc(*'MJPG')
        self._key_press = []
        recording_start_time = time.time()
        self._key_press_rec.append((self._key_press_rec_label(self._key_press_rec_iter),0))
        self._key_press_rec_iter+=1
        self.sound_thread = Thread(target=audio_record, args=[self.path+'/audio.wav'],daemon = True)
        self._video_color = cv2.VideoWriter(self.path + '/color.avi', codec_x264, 20, (self._kinect.color_frame_desc.Width, self._kinect.color_frame_desc.Height))
        self._video_depth = cv2.VideoWriter(self.path + '/depth.avi', codec_x264, 20, (self._kinect.color_frame_desc.Width, self._kinect.color_frame_desc.Height))
        self._video_infrared = cv2.VideoWriter(self.path + '/infrared.avi', codec_x264, 20, (self._kinect.color_frame_desc.Width, self._kinect.color_frame_desc.Height))
        #self.sound_thread = Thread(target=audio_record.start(self.path+'/audio.wav'), args=())
        #self.sound_thread.daemon = True
        self.sound_thread.start()
        variable_to_add_hotkey = keyboard.add_hotkey('ctrl+shift+t',add_key_press_rec,args=(time.time()-recording_start_time),timeout=1,trigger_on_release=False)
        self.hot_keys.append(variable_to_add_hotkey)

    def stopRecording(self):
        #audio_record.stop()
        subjID = ''
        aasanaID = ''
        self.audio_stop_flag = True
        while self.audio_is_stopped == False:
            pass
        self.audio_stop_flag = False
        self._video_color.release()
        self._video_depth.release()
        self._video_infrared.release()
        for v in self.hot_keys:
            keyboard.remove_hotkey(v)
        self.hot_keys = []
        self._key_press_rec=[0]
        self.write_key_press_rec()
        self.write_key_press()


    def recordingButton(self, start_msg, stop_msg, x, y, w, h, start_col, stop_col):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # print(click)
        if x + w > mouse[0] > x and y + h > mouse[1] > y and click[0] and self.prev_mouse_state == self.MOUSE_BUTTON_UP:
            if self.isRecording:
                self.stopRecording()
            else:
                self.ir_counter = 0
                self.depth_counter = 0
                self.startRecording()

            self.isRecording = not self.isRecording
            self.clicked = not self.clicked
            # pygame.draw.rect(screen, ac,(x,y,w,h))
        if self.clicked:
            msg = stop_msg
            col = stop_col
        else:
            msg = start_msg
            col = start_col
        pygame.draw.rect(self._screen, col, (x, y, w, h))

        self.prev_mouse_state = click[0]
        smallText = pygame.font.SysFont("comicsansms", 20)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        self._screen.blit(textSurf, textRect)

    def text_objects(self, text, font):
        textSurface = font.render(text, True, (0, 0, 0))
        return textSurface, textSurface.get_rect()

    def run(self):
        # -------- Main Program Loop -----------
        while not self._done:
            # --- Main event loop
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    self._done = True  # Flag that we are done so we exit this loop

                elif event.type == pygame.VIDEORESIZE:  # window resized
                    self._screen = pygame.display.set_mode(event.dict['size'],
                                                           pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE, 32)
                if event.type == pygame.KEYDOWN:
                    for c in range(ord('a'), ord('z')+1):
                        if event.key == c:
                            self._key_press.append((chr(c), str(datetime.now())))
                    for c in range(ord('0'), ord('9')+1):
                        if event.key == c:
                            self._key_press.append((chr(c), str(datetime.now())))
                    if event.key == pygame.K_SPACE:
                        self._key_press.append(('space', str(datetime.now())))
                    if event.key == pygame.K_RETURN:
                        self._key_press.append(('return', str(datetime.now())))
            # --- Game logic should go here

            # --- Getting frames and drawing
            # --- Woohoo! We've got a color frame! Let's fill out back buffer surface with frame's data
            if self.isRecording:
                if not (self._kinect.has_new_color_frame() and self._kinect.has_new_depth_frame() and self._kinect.has_new_infrared_frame() and (self._bodies is not None)):
                    print('yo')
                    continue

            self.now = str(datetime.now().time())
            if self._kinect.has_new_color_frame():
                frame = self._kinect.get_last_color_frame()
                self.draw_color_frame(frame, self._frame_surface)

                if self.isRecording:
                    frame1 = frame.reshape(
                        (self._kinect.color_frame_desc.Height, self._kinect.color_frame_desc.Width, 4))
                    frame2 = cv2.cvtColor(frame1, cv2.COLOR_RGBA2RGB)
                    #print("Frame conversion: ", end-start)
                    self._video_frameno[0] += 1
                    self._timestamps[0].append([self._video_frameno[0], self.now])

                    if (len(self._timestamps[0]) == 10):
                        self.csv_writer(self.path + '/color_timestamps.csv', self._timestamps[0])
                        self._timestamps[0] = []

                    self._video_color.write(frame2)
                    #self.frames[self._video_frameno[0]%100] = frame2
                    #if(self._video_frameno[0]%100==0):
                        #np.savez('color_frame', frame2)

                    #print("Frame writing: ", end - start)

            if self._kinect.has_new_depth_frame() and self.isRecording:
                frame = self._kinect.get_last_depth_frame()
                frame1 = frame.reshape((self._kinect.depth_frame_desc.Height, self._kinect.depth_frame_desc.Width))
                # cv2.imshow('frame1', frame1)
                # cv2.waitKey(5)
                self._video_frameno[1] += 1
                self._timestamps[1].append([self._video_frameno[1], self.now])
                if (len(self._timestamps[1]) == 10):
                    self.csv_writer(self.path + '/depth_timestamps.csv', self._timestamps[1])
                    self._timestamps[1] = []
                # depth_file = open(self.depth_path + '/' + str(self.depth_counter) + '.npy', 'wb')
                # np.save(depth_file, frame1)
                # self.depth_counter += 1
                # depth_file.close()
                self._video_depth.write(frame1)



            if self._kinect.has_new_infrared_frame() and self.isRecording:
                frame = self._kinect.get_last_infrared_frame()
                frame1 = frame.reshape((self._kinect.infrared_frame_desc.Height, self._kinect.infrared_frame_desc.Width))
                # cv2.imshow('frame1', frame1)
                # cv2.waitKey(5)
                self._video_frameno[2] += 1
                self._timestamps[2].append([self._video_frameno[2], str(datetime.now().time())])
                if (len(self._timestamps[2]) == 10):
                    self.csv_writer(self.path + '/infrared_timestamps.csv', self._timestamps[2])
                    self._timestamps[2] = []

                # ir_file = open(self.ir_path + '/' + str(self.ir_counter) + '.npy', 'wb')
                # np.save(ir_file, frame1)
                # self.ir_counter += 1
                # ir_file.close()
                self._video_infrared.write(frame1)



            '''if self._kinect.has_new_audio_frame() and self.isRecording:
                frame = self._kinect.get_last_audio_frame()
                self._timestamps[1].append([self._video_frameno[1], self.now])
                if (len(self._timestamps[1]) == 10):
                    self.csv_writer(self.path + '/depth_timestamps.csv', self._timestamps[1])
                    self._timestamps[1] = []
                #self._video_depth.write(frame1)'''
            # --- Cool! We have a body frame, so can get skeletons
            if self._kinect.has_new_body_frame():
                self._bodies = self._kinect.get_last_body_frame()

            # --- draw skeletons to _frame_surface
            if self._bodies is not None:
                for i in range(0, self._kinect.max_body_count):
                    body = self._bodies.bodies[i]
                    if not body.is_tracked:
                        continue

                    joints = body.joints
                    joint_orientations = body.joint_orientations
                    # convert joint coordinates to color space
                    joint_points = self._kinect.body_joints_to_color_space(joints)
                    self.draw_body(joints, joint_points, SKELETON_COLORS[i])
                    if self.isRecording:
                        self.store_joints(joints, joint_orientations, joint_points, i)

            # --- copy back buffer surface pixels to the screen, resize it if needed and keep aspect ratio
            # --- (screen size may be different from Kinect's color frame size)
            h_to_w = float(self._frame_surface.get_height()) / self._frame_surface.get_width()
            target_height = int(h_to_w * self._screen.get_width())
            surface_to_draw = pygame.transform.scale(self._frame_surface, (self._screen.get_width(), target_height));
            self._screen.blit(surface_to_draw, (0, 0))
            surface_to_draw = None
            self.recordingButton("Start", "Stop", 30, 30, 85, 45,  (0, 0, 255), (0, 255, 0))
            pygame.display.update()

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            self._clock.tick(60)
            self._frameno = self._frameno + 1

            print(self._clock.get_fps())

        # Close our Kinect sensor, close the window and quit.
        self._kinect.close()

        pygame.quit()


__main__ = "Kinect v2 Body Game"
'''
try:
    os.makedirs("Snaps")
except OSError:
    pass
'''

game = BodyGameRuntime();
game.run();
