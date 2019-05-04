#file to record audio
#from pyaudio lecture
#Code modified from https://people.csail.mit.edu/hubert/pyaudio/

import pyaudio
import wave
from array import array
from struct import pack

###########################################################################
######################### Recording a WAV file ############################
###########################################################################
#takes in the name of the file and length of recording and returns a wave
#file
def record(outputFile, length):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = int(length)
    fileName = outputFile + ".wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT, input_device_index = 0,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open("songs/" + fileName, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()