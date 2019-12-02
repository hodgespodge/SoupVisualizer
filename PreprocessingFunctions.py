from scipy.io import wavfile
import numpy as np
from scipy import signal
import cv2
import matplotlib.pyplot as plt

np.set_printoptions(precision=3,edgeitems=5,suppress=True,linewidth=50)

def find_fundamental_frequency_of_tone(freqs, times, spectro):
    return spectro