import numpy as np
import parselmouth
import crepe
import os

np.set_printoptions(precision=3,edgeitems=5,suppress=True,linewidth=50)

def get_fundemental_frequency(wav_file_path):
    snd = parselmouth.Sound(wav_file_path)

    print("seconds of song * 44100 = ",len(snd))
    return snd.to_pitch()

def get_crepe_confidence(audio,rate=44100,step_size= 50):

    return crepe.predict(audio, rate,step_size=step_size, viterbi=True)

def create_16_bit_wav(songname):
    import wavio
    from scipy.io import wavfile

    rate, audio = wavfile.read("TestSongs/"+songname+".wav")

    wavio.write("TestSongs/16bit/"+songname+"_16.wav", audio.astype(np.int16), rate, sampwidth=2)
