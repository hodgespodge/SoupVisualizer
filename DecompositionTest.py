from scipy.io import wavfile
import numpy as np
import pylab as pl
from sklearn.decomposition import FastICA

from scipy.io import wavfile
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

rate, audio = wavfile.read("Nangs.wav")

audio = np.mean(audio, axis=1)

M = 1024

print("creating spectrogram")
freqs, times, spectro = signal.spectrogram(audio, fs=rate, window='hanning',nperseg=1024, noverlap=M - 100,detrend=False, scaling='spectrum')


def replaceZeroes(data):
  min_nonzero = np.min(data[np.nonzero(data)])
  data[data == 0] = min_nonzero
  return data

spectro = replaceZeroes(spectro)

spectro = np.log10(spectro)

print(spectro)
print(spectro.shape)
# A = np.array([[1, 1], [0.5, 2]])  # Mixing matrix
# X = np.dot(S, A.T)  # Generate observations
# # Compute ICA

ica = FastICA(n_components=10)

print("performing ica.fit_transform")
S_ = ica.fit_transform(spectro)  # Reconstruct signals
# print(S_.shape)

fig, ax = plt.subplots()
ax.plot(S_[1], S_[0])
ax.set_xlabel('Time [s]')
ax.set_ylabel('Signal amplitude');

# print(type(S_))
# print(S_)

print("Performing ica.mixing_")
A_ = ica.mixing_  # Get estimated mixing matrix

print("plotting")

print("done")