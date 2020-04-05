from scipy.io.wavfile import read
from random import randint
from numpy import fft
import pygame, sys, time, os
from PreprocessingFunctions import *
import crepe
import scipy.signal
import pickle
import librosa


stem_dir = '5stems'
song = 'Let It Be'
instrument = 'vocals'

song_instrument = song + "_" + instrument + "_16-bit.wav"

vocal_file = os.path.join('SpleeterOutputs_16-bit',
                          stem_dir,
                          song + "_vocals_16-bit.wav")

drums_file = os.path.join('SpleeterOutputs_16-bit',
                          stem_dir,
                          song + "_drums_16-bit.wav")

song_file = os.path.join('TestSongs','16bit',song+'_16.wav')

def main():

    frame_rate = 44100

    rate, vocal_amplitude = read(vocal_file)
    rate2, drum_amplitude = read(drums_file)


    try:
        pickle_in = open("pickles/"+song+"_beats.pickle","rb")
        beat_times, tempo = pickle.load(pickle_in)

    except:

        print("Creating new beat and tempo information for " + song)

        y,sr = librosa.load(song_file)

        tempo, beat_frames = librosa.beat.beat_track(y = y,sr = sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)

        pickle_output = open("pickles/" + song + "_beats.pickle", "wb")
        pickle.dump((beat_times , tempo),pickle_output)
        pickle_output.close()


    print("estimated tempo",tempo)

    print("length of drum_amplitude",len(drum_amplitude))

    print("len amplitude before frame skip",len(vocal_amplitude))

    animation_fps = 20

    display_interval_ms = 1000/animation_fps
    display_interval_s = display_interval_ms/1000

    print("display_interval in ms: ", display_interval_ms)

    try:

        pickle_in = open("pickles/"+song+"_crepe.pickle","rb")
        crepe_stuff = pickle.load(pickle_in)
        crepe_vocal_time, crepe_vocal_frequency, crepe_vocal_confidence, crepe_vocal_activation = \
            crepe_stuff[0],crepe_stuff[1],crepe_stuff[2],crepe_stuff[3]

    except:

        print("Creating new vocal information for "+song)

        # Crepe returns vocal fundemental frequency info
        crepe_vocal_time, crepe_vocal_frequency, crepe_vocal_confidence, crepe_vocal_activation = get_crepe_confidence(vocal_amplitude, rate,step_size=display_interval_ms)

        pickle_output = open("pickles/"+song+"_crepe.pickle","wb")
        pickle.dump((crepe_vocal_time, crepe_vocal_frequency, crepe_vocal_confidence, crepe_vocal_activation),pickle_output)
        pickle_output.close()


    # graphic interface dimensions
    width, height = 840, 720
    center = [width // 2, height // 2]

    frame_skip = 96
    vocal_amplitude = vocal_amplitude[:, 0] + vocal_amplitude[:, 1]
    vocal_amplitude = vocal_amplitude[::frame_skip]
    frequency = list(abs(fft.fft(vocal_amplitude)))

    # print("fundemental freq list",len(get_fundemental_frequency(file_name).selected_array['frequency']))

    # scale the amplitude to 1/4th of the frame height and translate it to height/2(central line)
    # max_amplitude = max(vocal_amplitude)
    # for i in range(len(vocal_amplitude)):
    #     vocal_amplitude[i] = float(vocal_amplitude[i]) / max_amplitude * height / 4 + height / 2
    # vocal_amplitude = [int(height / 2)] * width + list(vocal_amplitude)

    while(True): #Wait for user to specify run
        play =  input()
        if play == "1":
            break

    pygame.init()
    # screen = pygame.display.set_mode([width, height])
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = pygame.display.get_surface().get_size()

    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.mixer.init()
    pygame.mixer.music.load(song_file)
    pygame.mixer.music.play()
    now = time.time()

    def remove_confidence_outliers(confidence):

        return scipy.signal.medfilt(confidence)

    crepe_vocal_confidence = remove_confidence_outliers(crepe_vocal_confidence)

    max_frequency = max(crepe_vocal_frequency)

    from math import log2, pow
    ##https: // www.johndcook.com / blog / 2016 / 02 / 10 / musical - pitch - notation /

    #############
    def pitch(freq):
        A4 = 440
        C0 = A4 * pow(2, -4.75)
        pitch_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

        h = round(12 * log2(freq / C0))
        octave = h // 12
        n = h % 12
        return pitch_names[n] + str(octave)

    #############

    def display_vocals(index):
        if crepe_vocal_confidence[index] > 0.75:
            # color = [255 * crepe_vocal_frequency[i]/max_frequency,255 * crepe_vocal_frequency[i]/max_frequency ,255 * crepe_vocal_frequency[i]/max_frequency]
            color = [200, 100, 255]

            note_frequency = crepe_vocal_frequency[index]

            print(note_frequency)

            pygame.draw.circle(screen,
                               color,
                               (int(width / 2), int((3 * height / 4) - note_frequency)),
                               50,
                               0)

            font = pygame.font.SysFont('Calibri',35,True,True)
            text = font.render(pitch(note_frequency),True,(255,255,255))
            screen.blit(text,[100,240])


    def display_drums():

        color = [100, 200, 255]

        try:
            drum_hit = abs((drum_amplitude[int(t * 44100)][0] + drum_amplitude[int(t * 44100)][1])//200)

            # print(int(t * 44100))
            if drum_hit > 30:

                pygame.draw.circle(screen,
                                   color,
                                   (int(width / 3), int(3 * height / 4)),
                                   drum_hit,
                                   0)
        except:
            pass


    color = [200,100,255]



    beat_times_index = 0
    for i,t in enumerate(crepe_vocal_time):

        screen.fill([0, 0, 0])
        pygame.event.get()

        player_time = pygame.mixer.music.get_pos()/1000

        if player_time > t:
            continue

        # try:

        display_vocals(index = i)
        # display_drums()


        #metronome

        if beat_times[beat_times_index] < player_time + 0.05:

            pygame.draw.circle(screen,
                               color,
                               (int(2 * width / 3), int(3 * height / 4)),
                               50,
                               0)
            beat_times_index += 1



        time.sleep(display_interval_s)

        pygame.display.update()
        # except:
        #     pass

if __name__ == '__main__':
    main()