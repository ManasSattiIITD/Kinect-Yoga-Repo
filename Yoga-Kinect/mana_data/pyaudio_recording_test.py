import pyaudio
# import sys
import wave

chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS, 
                rate=RATE, 
                input=True,
                output=True,
                frames_per_buffer=chunk)

import math

print("* recording")
frames = []
for i in range(0, math.ceil(44100 / chunk * RECORD_SECONDS)):
    data = stream.read(chunk)
    frames.append(data)
    # check for silence here by comparing the level with 0 (or some threshold) for 
    # the contents of data.
    # then write data or not to a file

print("* done")

stream.stop_stream()
stream.close()
p.terminate()
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()


# print(44100 / chunk * RECORD_SECONDS)
