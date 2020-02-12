import sys
import AudioPredictor as ap
#from pydub import AudioSegment
from scipy.io import wavfile
import wave as wv
#from pydub.playback import play
#from PyQt5.QtWidgets import QApplication, QLabel
#import os
#import AudioInput as ai
import numpy as np
#import tensorflow as tf
import random
from keras.models import Sequential, Model
from keras.layers import Dense, Flatten, Conv1D, Dropout, MaxPooling1D
import keras
#import matplotlib.pyplot as plt

#song = AudioSegment.from_wav("./amalgum/UMAPiano-DB-A0C#3Eb3-ST-M.wav")
#play(song)

#bpm = sys.argv[1]
#bad, data = wavfile.read("./audioFile.wav")
#path = "./A2Eb3G4-ST-M.wav"


def predictions(path, bpm, epochs):
    audio = wv.open(path)
    bad, data = wavfile.read(path)
    total_time = float(audio.getnframes())/float(audio.getframerate()) #sec
    
    predicNums = int(2*int(bpm)*total_time/60) # <-here is where I used a note factor
    if predicNums == 0:
    	predicNums=1
    predic_Size = int((total_time*audio.getframerate())/predicNums) #samples
    print("total time: " +str(total_time))
    print("predicNums: " +str(predicNums))
    print("totalSize: "+str(audio.getnframes()))
    #(V) samples per prediction
    print("PredicSize: "+str(predic_Size))
    #print("PredicSize (seconds)" + str(predic_Size/audio.getframerate()))
    #print("nframes: "+str(audio.getnframes()))

    #samp size when testing was 14500
    #epoch num should be proportional to bpm. The smaller the samples, the more training is necessary

    if epochs == 0:
        model = ap.loadModel("firstev")
    else:
        model = ap.everything(int(predic_Size), epochs, "firstev")
    #model = ap.loadModel("modelIndex600")

    #sampRate = bpm*4 or bpm*8
    #sampSize(sec) = total_samps/sampRate
    #8 predictions/beat
    #bpm*minutes = #beats
    #beats*8=preds
    #preds = 8*bpm*time(minutes)
    #frames/framerate = time
    #time*sampRate = samples
    #total time/#of predictions = size of 1 prediction

    #for each prediction
    #predicNums = 8*int(bpm)*total_time
    #loop goes through each prediction
    ansArr = np.empty(108)
    ansArr = np.expand_dims(ansArr, axis=0)
    for i in range(0,int(predicNums)):
        #print("predic_Nums: "+str(predicNums))
        #split audio into [samplesize*i:samplesize*(1+1)]
        #print("i: "+str(i))
        #print("predic_Size: "+str(predic_Size))
        tempData = data[int(predic_Size*i):int(predic_Size*(i+1))]
        #print("multiplic: "+str(predic_Size*i))
        #print("time: "+str(float(predic_Size*i)/float(audio.getframerate())))
        tempData = ap.regularize(tempData, predic_Size)
        #plt.plot(tempData)
        tempData = np.expand_dims(tempData, 0)
        tempData = np.expand_dims(tempData, 2)
        ans = model.predict(tempData)
        ans = np.squeeze(ans)
        #print(len(ans))
        ansArr = np.append(ansArr, np.expand_dims(ans, axis=0), axis=0)
        #plt.plot(ans)
        #print(ans)
        #plt.show()
        #plt.close()
    return ansArr
#arr = predictions("./A2Eb3G4-ST-M.wav", 2)
#print(arr.shape)
#print(len(arr))
#for i in range(0, len(arr)):
#    plt.plot(arr[i])
#    plt.show()
