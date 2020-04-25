import numpy as np
import pickle
import librosa

np.set_printoptions(precision=3,edgeitems=5,suppress=True,linewidth=50)

def get_fundemental_frequency(wav_file_path):
    import parselmouth
    snd = parselmouth.Sound(wav_file_path)

    return snd.to_pitch()

def create_16_bit_wav(songpath,outpath):
    import wavio
    from scipy.io import wavfile

    rate, audio = wavfile.read(songpath)

    wavio.write(outpath, audio.astype(np.int16), rate, sampwidth=2)

def create_pickle(file_name,data):

    print("creating pickle for",file_name)

    #empty file if already exists
    pickle_output = open("pickles/" + file_name, "wb")
    pickle_output.close()

    #dump data in file
    pickle_output = open("pickles/" + file_name, "wb")
    pickle.dump(data, pickle_output)
    pickle_output.close()
    print("done creating pickle")


def create_new_beat_tempo_profile(song_path, song_name):

    print("Creating new beat and tempo information for " + song_name)

    y, sr = librosa.load(song_path)

    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr,trim=False)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    create_pickle(song_name + "_beats.pickle",(beat_times, tempo))

    return beat_times, tempo

def create_new_ellipse_profile(song_name,vocal_amplitude,other_amplitude,num_points,screenL = 1980,screenH=1080,animation_frames = []):

    print("Creating Ellipse profile")

    import math
    import EllipseGeneration

    point_times = []

    for i,audio_frame in enumerate(animation_frames):

        if i % 100 == 0:
            print((audio_frame/len(vocal_amplitude)) * 100,"%")

        a = 1
        b = 1
        n1 = 1
        n2 = 1
        n3 = 1
        m = 4 #Number of corners on shape

        audio_frame = math.floor(audio_frame)

        n1 = ((abs(vocal_amplitude[audio_frame][0] + vocal_amplitude[audio_frame][1])) * 2 / 1000)
        n2 = n1
        n3 = ((abs(other_amplitude[audio_frame][0] + other_amplitude[audio_frame][1])) / 1000) + 3

        last_variables = (a,b,n1,n2,n3,m)

        radii = EllipseGeneration.Supershape(a, b, m, n1, n2, n3, num_points=num_points)

        point_times.append(EllipseGeneration.drawShapes(radii, screenL / 2, screenH / 2, 2, math.floor(i / 2), screenL))

    create_pickle(song_name + "_ellipses.pickle", (point_times))

    print("done ")

    return point_times
