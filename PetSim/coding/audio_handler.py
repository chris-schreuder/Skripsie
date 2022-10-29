from numpy import float32, float64
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import os
import pandas as pd


# Sampling frequency
fs = 32000
# Recording duration
duration = 2


def getRecCount(name):
    max_num = 0
    for audio in os.listdir('audio/' + name):
        if name in audio:
            audio = audio.replace('.wav', '')
            num = audio[len(name):len(audio)]
            num = int(num)
            if num >= max_num:
                max_num = num
    return str(max_num + 1)


def rec(name):
    print(name)
    try:
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype=float32)
        print("recording shape:")
        print(recording.shape)
        sd.wait()
        if name == 'command':
            file_name = "audio/command.wav"
            write(file_name, fs, recording)
            return 'Command successfully recorded.'
        elif name == 'name':
            file_name = "audio/name/name" + getRecCount(name) + ".wav"
            write(file_name, fs, recording)
            return 'Name successfully recorded.'
        else:
            file_name = "audio/" + name + "/" + name + getRecCount(name) + ".wav"
            write(file_name, fs, recording)
        return name + ' successfully recorded.'
    except:
        return name + ' did not record recorded.'
