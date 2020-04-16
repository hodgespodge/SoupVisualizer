import numpy as np
import crepe
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

    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    create_pickle(song_name + "_beats.pickle",(beat_times, tempo))

    return beat_times, tempo

def create_new_other_profile(y,sr,song_path,song_name,display_interval_ms):
    import librosa

    print("Creating new other profile")
    y, sr = librosa.load(song_path)

    pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)

    create_pickle(song_name + "_other.pickle", (pitches, magnitudes))

    return pitches,magnitudes

def create_new_vocal_profile(rate,vocal_amplitude,display_interval_ms,song_name):

    print("Creating new vocal information for " + song_name)

    # Crepe returns vocal fundamental frequency info
    import crepe

    crepe_vocal_time, crepe_vocal_frequency, crepe_vocal_confidence, crepe_vocal_activation = \
        crepe.predict(audio=vocal_amplitude,sr=rate,step_size=display_interval_ms,viterbi=True)

    create_pickle(song_name + "_vocal.pickle", (crepe_vocal_time, crepe_vocal_frequency, crepe_vocal_confidence,
                                                crepe_vocal_activation))

    return crepe_vocal_time, crepe_vocal_frequency, crepe_vocal_confidence, crepe_vocal_activation

def slope(X, Y):

    Y = list(Y)

    xbar = sum(X) / len(X)
    ybar = sum(Y) / len(Y)
    n = len(X)  # or len(Y)

    numerator = sum([xi * yi for xi, yi in zip(X, Y)]) - n * xbar * ybar
    denominator = sum([xi ** 2 for xi in X]) - n * xbar ** 2

    b = numerator / denominator

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
            #rounds the vocal confidence so animations are less eratic
            crepe_vocal_confidence[i] = average_confidence

        elif con_slope - (2/(3*average_confidence * average_confidence)) > threshold  :

            #updates vocal confidence to better match steep onsets
            crepe_vocal_confidence[i] = threshold + 0.1*(average_confidence * average_confidence* con_slope)%10

        else:

            crepe_vocal_confidence[i] = average_confidence

    return crepe_vocal_confidence

def group_vocals(window_size, threshold,crepe_vocal_frequency,crepe_vocal_confidence,crepe_vocal_time):

    time_between_distinct_clusters = 0.75
    vocal_times = []
    last_vocal_time = -1000
    vocal_bin = []
    min_vocal_segment_length = 1

    for i in range(len(crepe_vocal_time)):

        if crepe_vocal_confidence[i] > threshold:

            if crepe_vocal_time[i] - last_vocal_time > time_between_distinct_clusters:
                vocal_times.append(vocal_bin)
                vocal_bin = []

            vocal_bin.append((crepe_vocal_time[i],i))
            last_vocal_time = crepe_vocal_time[i]

    vocal_times.pop(0)

    i = 0
    while i < len(vocal_times):

        #if the vocal segment is too short, try and append it to another vocal segment.
        if(vocal_times[i][-1][0] - vocal_times[i][0][0] ) < min_vocal_segment_length:

            distance_to_lower = vocal_times[i][0][0]  - vocal_times[i -1][-1][0]
            distance_to_upper = vocal_times[i + 1][0][0]  -  vocal_times[i][-1][0]

            if distance_to_upper < time_between_distinct_clusters * 2 or distance_to_lower < time_between_distinct_clusters * 2:

                if distance_to_lower < distance_to_upper :

                    vocal_times[i-1 ] = vocal_times[i-1] + vocal_times[i]
                else:
                    vocal_times[i + 1] = vocal_times[i] + vocal_times[i + 1]

            del vocal_times[i]
        i+= 1

    for i,vocal_segment in enumerate( vocal_times):
        for time in vocal_segment:
            if crepe_vocal_confidence[time[1]] < 0.75 and crepe_vocal_confidence[time[1]] > 0.5:
                crepe_vocal_confidence[time[1]] = 0.76

    return crepe_vocal_confidence

def create_new_ellipse_profile(song_name,vocal_amplitude,other_amplitude,screenL = 1980,screenH=1080,animation_frames = []):

    print("Creating Ellipse profile")

    import math
    import PygameExperimentation

    point_times = []

    for i,audio_frame in enumerate(animation_frames):

        if i % 100 == 0:
            print((audio_frame/len(vocal_amplitude)) * 100,"%")

        a = 1
        b = 1
        n1 = 1
        n2 = 1
        n3 = 1
        m = 4

        audio_frame = math.floor(audio_frame)

        n1 = ((abs(vocal_amplitude[audio_frame][0] + vocal_amplitude[audio_frame][1])) * 2 / 1000)
        n2 = n1
        n3 = ((abs(other_amplitude[audio_frame][0] + other_amplitude[audio_frame][1])) / 1000) + 3

        last_variables = (a,b,n1,n2,n3,m)

        radii = PygameExperimentation.Supershape(a,b,m,n1,n2,n3)

        point_times.append(PygameExperimentation.drawShapes(radii,screenL/2,screenH/2,2, math.floor(i/2) ,screenL))

    create_pickle(song_name + "_ellipses.pickle", (point_times))

    print("done ")

    return point_times
