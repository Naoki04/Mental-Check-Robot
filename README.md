# Eyesight-Direction-Estimation
Group Project for Bio-inspired Artificial Intelligence class on Msc Biorobotics in University of Bristol.



## Eyesight direction tracking
### Demo:
 https://youtu.be/htRZiP4whYc


### Ref GitHub: 
https://github.com/gakutosasabe/OpenCVEyeTracking

### Trained model for dlib
http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2

### Setup and test
Download trained model and place at "/eyesight-tracking/OpenCVEyeTracking/shape_predictor_68_face_landmarks.dat" before setup.
```
$ pyenv global system
$ sudo apt-get install python3-tk
$ sudo apt install tk-dev

$ pyenv install python==3.6
$ pip install opencv-python==4.6.0.66
$ pip install cmake
$ pip install dlib
$ cd eyesight-tracking/OpenCVEyeTracking
$ python eyetracking.py
```
※ I tried on Ubuntu 22.04

Note: dlib sometimes have error on installation. We need cmake before installing dlib. dlib only support python<=3.6, so we need pyenv if on ubuntu. (conda for Arm Ubuntu doesn't support python<=3.6)

Help for error on tkinter on pyenv: https://www.python.ambitious-engineer.com/archives/357


![demo](eyesight-tracking/OpenCVEyeTracking/eyetracking-demo.png)

