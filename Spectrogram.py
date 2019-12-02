from scipy.io import wavfile
import numpy as np
from scipy import signal

import cv2


rate, audio = wavfile.read('BigShip.wav')

audio = np.mean(audio, axis=1)

M = 1024

print("creating spectrogram")
freqs, times, spectro = signal.spectrogram(audio, fs=rate, window='hanning',nperseg=1024, noverlap=M - 100,detrend=False, scaling='spectrum')
print("made spectrogram")

print("len(freqs)",len(freqs))
print("len(times)",len(times))

# spectro = np.swapaxes(spectro,0,1)
print(spectro.shape)

np.set_printoptions(precision=3,edgeitems=10,suppress=True,linewidth=100000)
# print(spectro.astype(int))

spectro = np.log10(spectro)
spectro = spectro.astype(np.uint8)

print(spectro)

ret, thresh = cv2.threshold(spectro,127,255,0)

print("Running cv2.findcontours")

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

color = cv2.cvtColor(spectro, cv2.COLOR_GRAY2BGR)

img = cv2.drawContours(color, contours, -1, (0,255,0), 2)
cv2.imshow("contours", color)
cv2.waitKey()
cv2.destroyAllWindows()