from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QLineEdit
import pyqtgraph as pg
#import matplotlib
import matplotlib.pyplot as plt
import sys
import AudioInput as ai
import FilePlayer as fp
#import timeit
import time
from pydub import AudioSegment
from pydub.playback import play
import pygame
import imageio
import os
#import scipy.misc

class AudioPlayer(QWidget):

    def __init__(self):
        super(AudioPlayer, self).__init__()
        self.paused = False
        self.audio = None
        self.started = False
        #self.i =0
        self.init = 0
        self.initUI()

    def filePop(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './\\',"WAV files (*.wav)")
        self.audioPath = fname[0]
        self.fileDisp.setText(fname[0])
        self.fileDisp.adjustSize()
        self.audio = AudioSegment.from_wav(fname[0])
        pygame.init()
        pygame.mixer.music.load(self.audioPath)
    
    def play(self):
        self.paused = False
        #modify predictions to return array full of predictions
        #after array has been loaded start audio file
        #make prediction
        #wait the length of one sample-time to predict
        #repeat
        bpm = 9
        epochs = 15
        try:
            #print(int(self.bpmField.text()))
            bpm = int(self.bpmField.text())
        except:
            print("enter correct nimber")
        try:
            epochs = int(self.epochField.text())
            print("HERE, epochs" + str(epochs))
        except:
        	print("enter correct epoch")

        print("here")
        audio_length = len(self.audio) #in milisecs
        #here's where model is created and an array full of predictions for each frame
        ansArr = fp.predictions(self.audioPath, bpm, epochs)
        picArr = []
        c = 0
        timeConst = audio_length/len(ansArr)
        print("this value is the amount of time between each frame (in milisec): "+str(timeConst))
        for i in ansArr:
        #i is a singular answer array
        	plt.plot(i)
        	for x in range(0, len(i)):
        		
        		if i[x] > .6:
        			#print(i[x])
        			#print(ai.findNote(x))
        			plt.annotate(ai.findNote(x), (x, i[x]))
        			#note, (x,y))
        		
        	c+=1
        	#total length of audio
        	#number of predictions
        	#length (mili)/#of predictions = length of 1 prediction
        	#length of 1 * i = time?
       		#replace C with a time stamp
       		tim = timeConst*c
       		
       		plt.savefig('./pics/'+str(c)+" "+str(tim/1000)+'.png')
       		plt.clf()
        
        #converts pictures into gif
        images = []
        for subdir, dir, files in os.walk('./pics/'):
        	#print(files)
        	for filename in sorted(files):
        		#print(os.getcwd())
        		if filename.endswith('.png'):
        			images.append(imageio.imread(os.getcwd()+'/pics/'+filename, format='png'))
        imageio.mimsave('./pics/movie.gif',images)
        

        delayTime = float(audio_length)/float(len(ansArr)-.009) #total time / len(ansArr) = time/ans
        print("delayTime: " +str(float(delayTime)/1000))
        
        if not self.started:
            pygame.mixer.music.play()
            self.started = True
        else:
            pygame.mixer.music.unpause()
        i = self.init
        while i<len(ansArr):
            #print(i)
        #for i in range(0,len(ansArr)):
            #print(self.i)
            if not self.paused:
                #start = time.time()
                self.predic_Plot.clear()
                self.predic_Plot.plot(ansArr[i])
                QApplication.processEvents()
                #end = time.time()
                #print(end-start)
                #pg.QtGui.processEvents()
                time.sleep(float(delayTime)/1000)
                i =i+1
                #print("after sleep")
            else:
                self.init = i
                break
            #print("hello")
            #self.i=0
        self.started = False
        self.init = 0
        #print("play") 
        

    def pause(self):
        pygame.mixer.music.pause()
        self.paused = True
        #print("pause")

    def initUI(self):

        self.predic_Plot = pg.PlotWidget(parent = self)
        self.predic_Plot.resize(800,600)
        self.predic_Plot.move(150, 50)
        
        self.bpmField = QLineEdit('bpm',self)
        self.bpmField.move(0,150)

        self.epochField = QLineEdit('epochs', self)
        self.epochField.move(0,190)
        
        self.dlgBtn = QPushButton("Open File", self)
        self.fileDisp = QLabel("file",self)
        self.fileDisp.move(10,120)
        self.dlgBtn.clicked.connect(self.filePop)
        self.playBtn= QPushButton("Play", self)
        self.playBtn.move(0,80)
        self.playBtn.clicked.connect(self.play)
        self.pauseBtn= QPushButton("Pause", self)
        self.pauseBtn.move(0,40)
        self.pauseBtn.clicked.connect(self.pause)

        self.resize(1000,700)
        log = QFileDialog(self)
        self.show()

app = QApplication(sys.argv)
wind = AudioPlayer()
sys.exit(app.exec_())