from scipy.io import wavfile
import numpy as np
from scipy import signal
import cv2
import matplotlib.pyplot as plt
from sklearn import preprocessing

np.set_printoptions(precision=3,edgeitems=5,suppress=True,linewidth=50)

def find_fundamental_frequency_of_tone(freqs, times, spectro):
    return spectro

'''
As far as I can tell, spacing on harmonics determins the fundemental frequency.
The challenge then is in identifying the spacing, finding the fundemental frequency, 
then elimating the other tones. 



'''