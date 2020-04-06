import numpy as np

import os

np.set_printoptions(precision=3,edgeitems=5,suppress=True,linewidth=50)

def get_fundemental_frequency(wav_file_path):
    import parselmouth
    snd = parselmouth.Sound(wav_file_path)

    print("seconds of song * 44100 = ",len(snd))
    return snd.to_pitch()

def get_crepe_confidence(audio,rate=44100,step_size= 50):
    import crepe

    return crepe.predict(audio, rate,step_size=step_size, viterbi=True)

def create_16_bit_wav(songpath,outpath):
    print("running create 16 bit wav")
    import wavio
    from scipy.io import wavfile

    rate, audio = wavfile.read(songpath)

    print("creating 16_bit wav file at",outpath)

    wavio.write(outpath, audio.astype(np.int16), rate, sampwidth=2)

def wav_to_mp3(songpath,outpath):
    from pydub import AudioSegment
    AudioSegment.converter = "C:\\ffmpeg\\bin\\ffmpeg.exe"
    AudioSegment.ffmpeg = "C:\\ffmpeg\\bin\\ffmpeg.exe"
    AudioSegment.ffprobe = "C:\\ffmpeg\\bin\\ffprobe.exe"


    sound = AudioSegment.from_mp3(songpath)
    sound.export(outpath, format="wav")

# wav_to_mp3("TestSongs/Weird Fishes.mp3","TestSongs/Weird Fishes.wav")