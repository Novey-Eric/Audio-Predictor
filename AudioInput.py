#import matplotlib.pyplot as plt
#from scipy.fftpack import fft
#from scipy.io import wavfile
#import scipy
#from scipy.signal import find_peaks
#from scipy import signal
#import wave
import numpy as np
import os
import re
#wav files have 1 channel and 2 bytes sampwidth

def findNote(freq):
    if freq < 0:
        freq = abs(freq)%12
        freq = 12-abs(freq)
    else:
        freq = (freq+3)%12
    switch ={
            0: 'A',
            1: 'A#',
            2: 'B',
            3: 'C',
            4: 'C#',
            5: 'D',
            6: 'D#',
            7: 'E',
            8: 'F',
            9: 'F#',
            10: 'G',
            11: 'G#',
            12: 'A'
            }
    return switch.get(freq, "bad")

class chord:
    def __init__(self, notes):
        self.notes = notes
        self.name = ""
    def __str__(self):
        out = []
        for i in self.notes:
            out.append(i)
        return out

    
def getNote(self, freq):
    numHalfs = math.log10(freq/440)/math.log10(2**(1/12))


#def noteFromFile(self, filePath)
def readNotes(path):


    #i think everything above here is useless
    regEx3 = "DB-(?P<first>[A-G].?[0-9])(?P<second>[A-G].?[0-9])?(?P<third>[A-G].?[0-9])?"
    betterRegEx = "([A-G].?[0-9])"
    fileNotes = re.findall(betterRegEx, path)
    #fileNotes = re.search(regEx3, path)
    noteDict = {
        "A": 9,
        "B": 11,
        "C": 0,
        "D": 2,
        "E": 4,
        "F": 5,
        "G": 7
           }

    allNotesArr = np.zeros(108)
    #allNotesArr = np.zeros(12)
    #index 57 is A4

    for val in fileNotes:
        if len(val) == 2:
                octave = int(val[1:2])
                note = val[0:1]
                awayFromA = noteDict[note]
                intoBin = awayFromA#+(12*octave)
        else:
            octave = int(val[2:3])
            note = val[0:1]
            acc = val[1:2]
            awayFromA = noteDict[note]
            if acc=="#":
                intoBin = (awayFromA+1)+(12*octave)
            elif acc=="b":
                intoBin = (awayFromA-1)+(12*octave)
        allNotesArr[intoBin] = 1
    
    #print(notes)
    #print(finalNotes)
    #print(allNotesArr)
    #plt.show()
    
    return allNotesArr
#print(readNotes(".9Notes/UMAPiano-DB-Poly-9-C/UMAPiano-DB-C1E1G1B1C2E2G2B2C3-NO-M"))
#print(readNotes("./2Notes/Fifth/UMAPiano-DB-Poly-2-Fifth-A/UMAPiano-DB-A0E1-NO-P.wav"))
#readNotes("./3Notes/UMAPiano-DB-Poly-3-A/UMAPiano-DB-A0A2C3-PE-F.wav")
