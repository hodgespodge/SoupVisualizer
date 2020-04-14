import numpy as np
import crepe
import pickle
import librosa

np.set_printoptions(precision=3,edgeitems=5,suppress=True,linewidth=50)

def get_fundemental_frequency(wav_file_path):
    import parselmouth
    snd = parselmouth.Sound(wav_file_path)

    print("seconds of song * 44100 = ",len(snd))
    return snd.to_pitch()

def create_16_bit_wav(songpath,outpath):
    import wavio
    from scipy.io import wavfile

    rate, audio = wavfile.read(songpath)

    wavio.write(outpath, audio.astype(np.int16), rate, sampwidth=2)

def create_new_beat_tempo_profile(song_path, song_name):

    print("Creating new beat and tempo information for " + song_name)

    y, sr = librosa.load(song_path)

    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)


    #first empty the file if it exists already
    pickle_output = open("pickles/" + song_name + "_beats.pickle", "wb")
    pickle_output.close()


    pickle_output = open("pickles/" + song_name + "_beats.pickle", "wb")

    pickle.dump((beat_times, tempo), pickle_output)
    pickle_output.close()

    return beat_times, tempo

def create_new_vocal_profile(rate,vocal_amplitude,display_interval_ms,song_name):

    print("Creating new vocal information for " + song_name)

    # Crepe returns vocal fundamental frequency info
    import crepe

    crepe_vocal_time, crepe_vocal_frequency, crepe_vocal_confidence, crepe_vocal_activation = \
        crepe.predict(audio=vocal_amplitude,sr=rate,step_size=display_interval_ms,viterbi=True)

    crepe_vocal_confidence= adjust_vocal_onset_confidence(window_size=20, threshold=0.75, crepe_vocal_frequency=crepe_vocal_frequency,
                                  crepe_vocal_confidence=crepe_vocal_confidence, crepe_vocal_time=crepe_vocal_time)

    # first empty the file if it exists already
    pickle_output = open("pickles/" + song_name + "_crepe.pickle", "wb")
    pickle_output.close()

    pickle_output = open("pickles/" + song_name + "_crepe.pickle", "wb")

    pickle.dump((crepe_vocal_time, crepe_vocal_frequency, crepe_vocal_confidence, crepe_vocal_activation),
                pickle_output)
    pickle_output.close()

    return crepe_vocal_time, crepe_vocal_frequency, crepe_vocal_confidence, crepe_vocal_activation


def wav_to_mp3(songpath,outpath):
    from pydub import AudioSegment
    AudioSegment.converter = "C:\\ffmpeg\\bin\\ffmpeg.exe"
    AudioSegment.ffmpeg = "C:\\ffmpeg\\bin\\ffmpeg.exe"
    AudioSegment.ffprobe = "C:\\ffmpeg\\bin\\ffprobe.exe"


    sound = AudioSegment.from_mp3(songpath)
    sound.export(outpath, format="wav")

def create_new_ellipse_profile():
    return None

def slope(X, Y):

    Y = list(Y)

    xbar = sum(X) / len(X)
    ybar = sum(Y) / len(Y)
    n = len(X)  # or len(Y)

    numer = sum([xi * yi for xi, yi in zip(X, Y)]) - n * xbar * ybar
    denum = sum([xi ** 2 for xi in X]) - n * xbar ** 2

    b = numer / denum

    return b

def adjust_vocal_onset_confidence(window_size, threshold,crepe_vocal_frequency,crepe_vocal_confidence,crepe_vocal_time):

    for i in range(len(crepe_vocal_confidence)):
        frequency = crepe_vocal_frequency[i : i + window_size ]
        confidence = crepe_vocal_confidence[i : i +  window_size ]

        average_frequency = 0
        average_confidence = 0

        if len(confidence) > 0:

            average_frequency = sum(frequency)/len(frequency)
            average_confidence = sum(confidence)/len(confidence)

        con_slope = slope(crepe_vocal_time[i : i + window_size], confidence)

        if average_confidence > threshold:
            # print(crepe_vocal_time[i], str(round(average_frequency, 2)),str(round(average_confidence, 2))," <---------@@")

            #rounds the vocal confidence so animations are less eratic
            crepe_vocal_confidence[i] = average_confidence

        elif con_slope - (2/(3*average_confidence * average_confidence)) > threshold  :

            #updates vocal confidence to better match steep onsets
            crepe_vocal_confidence[i] = threshold + 0.1*(average_confidence * average_confidence* con_slope)%10

            # print(crepe_vocal_time[i],str(round(average_frequency, 2)),str(round(average_confidence, 2))," <-------",str(round(con_slope, 2)),str(round(crepe_vocal_confidence[i], 2)))

        else:

            crepe_vocal_confidence[i] = average_confidence

            # print(crepe_vocal_time[i],str(round(average_frequency, 2)),str(round(average_confidence, 2)))

    return crepe_vocal_confidence

def group_vocals(window_size, threshold,crepe_vocal_frequency,crepe_vocal_confidence,crepe_vocal_time):


    time_between_distinct_clusters = 1
    vocal_times = []
    last_vocal_time = -1000
    vocal_bin = []
    min_vocal_segment_length = 1

    for i in range(len(crepe_vocal_time)):

        if crepe_vocal_confidence[i] > threshold:

            if crepe_vocal_time[i] - last_vocal_time > time_between_distinct_clusters:
                vocal_times.append(vocal_bin)
                vocal_bin = []

            vocal_bin.append(crepe_vocal_time[i])
            last_vocal_time = crepe_vocal_time[i]

    vocal_times.pop(0)

    #TEST
    vocal_times.append([84.5,85.4])

    for item in vocal_times:
        print(item[0], item[-1])

    for i in range(len(vocal_times)):

        #if the vocal segment is too short, try and append it to another vocal segment.
        if(vocal_times[i][-1] - vocal_times[i][0]) < min_vocal_segment_length:

            distance_to_lower = vocal_times[i][0] - vocal_times[i -1][-1]
            distance_to_upper = vocal_times[i + 1][0] -  vocal_times[i][-1]

            print(distance_to_lower,distance_to_upper)

            if distance_to_lower > distance_to_upper:
                pass

            print(vocal_times[0],vocal_times[-1])







        # print(item[0],item[-1])

        # print(item)

import os
from scipy.io.wavfile import read
song_name = "Creep .wav"
stem_dir = '5stems'

animation_fps = 60

display_interval_ms = 1000 / animation_fps

vocal_file = os.path.join('SpleeterOutputs_16-bit',
                              stem_dir,
                              song_name + "_vocals_16-bit.wav")

drums_file = os.path.join('SpleeterOutputs_16-bit',
                          stem_dir,
                          song_name + "_drums_16-bit.wav")

rate, vocal_amplitude = read(vocal_file)
rate2, drum_amplitude = read(drums_file)

try:
    pickle_in = open("pickles/" + song_name + "_beats.pickle", "rb")
    beat_times, tempo = pickle.load(pickle_in)

except:

    beat_times, tempo = create_new_beat_tempo_profile()

print("estimated tempo", tempo)
print("length of drum_amplitude", len(drum_amplitude))
print("len amplitude before frame skip", len(vocal_amplitude))

try:

    pickle_in = open("pickles/" + song_name + "_crepe.pickle", "rb")
    crepe_stuff = pickle.load(pickle_in)
    crepe_vocal_time, crepe_vocal_frequency, crepe_vocal_confidence, crepe_vocal_activation = \
        crepe_stuff[0], crepe_stuff[1], crepe_stuff[2], crepe_stuff[3]

except:

    # Crepe returns vocal fundemental frequency info
    crepe_vocal_time, crepe_vocal_frequency, crepe_vocal_confidence, crepe_vocal_activation = \
        create_new_vocal_profile(rate, vocal_amplitude, display_interval_ms, song_name)

crepe_vocal_confidence =  adjust_vocal_onset_confidence(window_size=20,threshold=0.75,crepe_vocal_frequency=crepe_vocal_frequency,crepe_vocal_confidence=crepe_vocal_confidence,crepe_vocal_time=crepe_vocal_time)

group_vocals(window_size=20,threshold=0.75,crepe_vocal_frequency=crepe_vocal_frequency,crepe_vocal_confidence=crepe_vocal_confidence,crepe_vocal_time=crepe_vocal_time)

