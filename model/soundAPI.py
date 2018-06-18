# -*- coding: utf-8 -*-
import pyaudio
import wave
import os

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5

def playSoundFromFile(filename):
    if (filename==""):
        return
    waveInputPath = "AUDIOS/" + filename
    p = pyaudio.PyAudio()
    wf = wave.open(waveInputPath, 'rb')
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True)
    data = wf.readframes(CHUNK)
    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    p.terminate()
    return
    
def getFrames(filename):
    if (filename==""):
        return []
    frames=[]
    waveInputPath = "AUDIOS/" + filename
    p = pyaudio.PyAudio()
    wf = wave.open(waveInputPath, 'rb')
    data = wf.readframes(CHUNK)
    while data:
        frames.append(data)
        data = wf.readframes(CHUNK)
    p.terminate()
    return frames
    
def playSoundFromFrames(frames):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True)
    i=0
    while (i < len(frames)):
        data = frames[i]
        stream.write(data)
        i+=1
    stream.stop_stream()
    stream.close()
    p.terminate()
    return

def recordSound():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    return frames
    
def saveSound(language, cardId, frames):
    p = pyaudio.PyAudio()
    waveOutputPath = language.upper()+str(cardId)+".wav"
    wf = wave.open("AUDIOS/"+waveOutputPath, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    p.terminate()
    return waveOutputPath
    
def deleteAudio(filename):
    if (filename==""):
        return
    os.remove("AUDIOS/"+filename)