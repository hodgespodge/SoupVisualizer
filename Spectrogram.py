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

def replaceZeroes(data):
  min_nonzero = np.min(data[np.nonzero(data)])
  data[data == 0] = min_nonzero
  return data

spectro = replaceZeroes(spectro)

spectro = np.log10(spectro)

print (spectro)

print()
print()

#------------------------------------
#
import matplotlib.pyplot as plt
f, ax = plt.subplots(figsize=(15, 15))
# plt.imshow(spectro ,aspect='auto')
# ax.invert_yaxis()
# plt.show()

#------------------------------------

spectro = spectro.astype(np.uint8)

print(spectro)

print("Running threshold function")

thresh = cv2.adaptiveThreshold(spectro,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

# blur = cv2.GaussianBlur(spectro,(5,5),0)
# ret,thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

print("Running cv2.findcontours")

plt.imshow(thresh,aspect='auto')
ax.invert_yaxis()
plt.show()

cv2.denoi

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)



color = cv2.cvtColor(spectro, cv2.COLOR_GRAY2BGR)
# cv2.imshow("graph without contours", color)
img = cv2.drawContours(color, contours, -1, (255,0,255), 1)
# cv2.imshow("graph with contours", color)

cv2.waitKey(0)
cv2.destroyAllWindows()