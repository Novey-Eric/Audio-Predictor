import os
import AudioInput as ai
import numpy as np
import tensorflow as tf
#import wave as wv
import random
from scipy.io import wavfile
from keras.models import Sequential, Model
from keras.layers import Dense, Flatten, Conv1D, Dropout, MaxPooling1D
import keras
import matplotlib.pyplot as plt

def regularize(tempData, sampSize):
    #tempData = tempData[11000:11000+sampSize]
    
    tempData = np.abs(np.fft.fft(tempData))
    tempData.resize(int(len(tempData)/2))
    tempData = tempData/np.amax(tempData)
    avg = np.average(tempData)
    tempData = tempData-avg
    return tempData

def createFiles(create, sampSize=14500, name=None):
    annotes = np.empty((0,108))
    twoNotesDir = "./2Notes"

    if create:
        for root, dirs, files in os.walk("./amalgum"):
            for i in files:
                annotes = np.append(annotes, np.expand_dims(ai.readNotes(os.path.join(root, i)),0), axis=0)
                #print(annotes.shape[0])
                if annotes.shape[0]>600:
                    break
        np.save(name, annotes)
    annotes = np.load("./"+name+".npy")

    fileDirs = np.empty((0,int(sampSize/2)))
    #print("samp/2")
    print(sampSize/2)
    if create:
        for root, dirs, files in os.walk("./amalgum"):
            for i in files:
                #print(i)
                #print(fileDirs.shape[0])
                bad, data = wavfile.read(root+"/"+i)
                #tempData = np.copy(data)
                tempData = data[11000:11000+sampSize]
                tempData = regularize(tempData, sampSize)

                fileDirs = np.append(fileDirs, np.expand_dims(tempData,0),axis=0)
                if fileDirs.shape[0]>600:
                    break
        np.save("fft"+name, fileDirs)
    fileDirs = np.load("./fft"+name+".npy")
    fileDirs = np.expand_dims(fileDirs,2)
    return (annotes, fileDirs)

def createModel():
    model = Sequential()
    model.add(Conv1D(2,3))
    model.add(MaxPooling1D())
    model.add(Dropout(.2))
    model.add(Flatten())
    model.add(Dense(300, activation = 'linear'))
    model.add(Dense(240, activation = 'relu'))
    model.add(Dense(190, activation = 'relu'))
    model.add(Dense(140, activation = 'relu'))
    model.add(Dropout(.1))
    model.add(Dense(108, activation = 'sigmoid'))
    return model

def loadModel(name):
    model = keras.models.load_model(name)
    return model

def saveModel(model, name):
    model.save(name)

def everything(sampSize, epochs, name):
    annotes, fileDirs = createFiles(True, sampSize, name)
    model = createModel()
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['mse'])
    model.fit(fileDirs, annotes, epochs=epochs, batch_size=25)
    saveModel(model, name)
    return model

#annotes, fileDirs = createFiles(False, name="108Index600")
#model = createModel()
#model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['mse'])
#model.fit(fileDirs, annotes, epochs=40, batch_size=25)
#saveModel(model, "modelIndex600")
#model = loadModel("modelIndex600")


def testFunc():

    for num in range(0,10):
        index = random.randint(0,600)
        print(index)
        for i in range(0, len(annotes[index])):
            print(str(i)+": "+ str(annotes[index][i]))
        dat = fileDirs[index]
        #t, dat = wavfile.read("./3Notes/UMAPiano-DB-Poly-3-C/UMAPiano-DB-E5Gb5C6-PE-P.wav")
        tempData = np.copy(dat)
        #tempData = regularize(tempData)
        tempData = np.expand_dims(tempData, 0)

        ans= model.predict(tempData)
        #ans = [0 if index <.001 for index in ans]
        #ans[ans<100000] = 0
        #ans[ans>.001] = 1
        print("ANSWER!!!!!!")
        for i in range(0, len(ans[0])):
            print(str(i)+ ": "+ str(ans[0][i]))
        plt.plot(ans[0])
        plt.plot(annotes[index])
        plt.show()
        #print(ans)
        #fileDirs are directory of training files, annotes are annotations
        
#testFunc()