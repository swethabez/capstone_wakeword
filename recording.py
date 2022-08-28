#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 12:55:49 2022

@author: mani
"""

import sounddevice as sd

import wavio as wv
import librosa
import numpy as np
import math
import soundfile
# Sampling frequency
freq = 44100

# Recording duration
duration = 5

start = 20
end = 25
name = 'Mani'


for i in range(start, end, 1):
    print('start')
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=1)

    # Record audio for the given number of seconds
    sd.wait()

    wv.write(name+str(i)+".wav", recording, freq, sampwidth=2)
    print('end')
    print(' ')



for i in range(end):
    signal, sr = librosa.load(name+str(i)+".wav", sr=16000)
    RMS=math.sqrt(np.mean(signal**2))
    STD_n= 0.1
    noise=np.random.normal(0, STD_n, signal.shape[0])
    signal_noise = signal + noise
    soundfile.write(name + 'noise' +str(i)+'.wav',signal_noise,16100)
