from scipy.io import wavfile
import numpy as np
from scipy import signal

import cv2


rate, audio = wavfile.read('Sweater.wav')

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

spectro = np.log10(spectro)


print (spectro)

print()
print()

spectro = spectro.astype(np.uint8)

print(spectro)

# #------------------------------------
#
# import matplotlib.pyplot as plt
# f, ax = plt.subplots(figsize=(15, 15))
# plt.imshow(spectro ,aspect='auto')
# ax.invert_yaxis()
# plt.show()
#
# #------------------------------------

ret, thresh = cv2.threshold(spectro,200,255,cv2.THRESH_TOZERO)
print("Running cv2.findcontours")

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

color = cv2.cvtColor(spectro, cv2.COLOR_GRAY2BGR)

cv2.imshow("graph without contours", color)

img = cv2.drawContours(color, contours, -1, (255,0,255), 1)

cv2.imshow("graph with contours", color)
cv2.waitKey(0)
cv2.destroyAllWindows()