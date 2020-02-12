# Audio-Predictor
This program aims to use a machine learning algorithm to predict notes being played in an audio file. This project was just an introduction to machine learning and TensorFlow for myself. It is in no way a perfect program, but I think it gets the job done.
# How to use
First download the zip file and extract the "amalgum" and "env" folders into the same folder as this project.
https://www.mediafire.com/file/i8v94n7xjxqyjt4/Archive.zip/file
Run the AudioGraphics.py file using the "env" python environment
Use the "open file" button to chose whichever file you want to learn the notes of.
The bpm does not need to be exact, you can think of it as more of a field that indicates the length of each prediction.
For example a 1 bpm field will have a much longer prediction than a 100 bpm field.
The "epochs" field is the number of traning epochs that the neural network will go through. A higher number for bpm will likely require a higher number of training epochs because of the small size of the prediction.
After the audio file starts playing, you can exit the program. It creates graphs of the predicted notes with timestamps as the name. This will be far more accurate than the real-time display.

### Problems
This project was a great way of learning more about fourier transforms and machine learning. Unfortunately, it seems this will likely not work very well for complex rhythms or really anything practical. I believe this comes down to the power of the fourier transform and the timeframe on which the operation occurs. I tried somewhat solving this problem using a bpm field but there probably needs to be a much more complex algorithm for when the transform occurs.
Secondly, the visual display of the graph does not synch with the music, so instead I would recommend quitting the program after it starts playing and using the image files it creates with timestamps.
Either way, I hope this helps someone :)
