from scipy.io.wavfile import read

import pygame, sys, time, os
from PreprocessingFunctions import *
import crepe
import scipy.signal
import pickle
import librosa
import math

animation_fps = 30

display_interval_ms = 1000 / animation_fps
display_interval_s = display_interval_ms / 1000

def create_instrument_charactaristics(song_path):

    print("creating instrument charactaristics")

    stem_dir = '5stems'
    song_name = os.path.basename(song_path)

    vocal_file = os.path.join('SpleeterOutputs_16-bit',
                              stem_dir,
                              song_name + "_vocals_16-bit.wav")

    other_file = os.path.join('SpleeterOutputs_16-bit',
                              stem_dir,
                              song_name + "_other_16-bit.wav")

    rate_vocal, vocal_amplitude = read(vocal_file)
    rate_other, other_amplitude = read(other_file)


    num_samples = len(vocal_amplitude)

    animation_frames = []

    for i in range(math.floor((num_samples*animation_fps)/44100)):
        animation_frames.append(int(i * 44100/ animation_fps))

    print("these are the frames to animate on:",animation_frames)

    # crepe_vocal_time, crepe_vocal_frequency, crepe_vocal_confidence, crepe_vocal_activation = \
    #     create_new_vocal_profile(rate_vocal, vocal_amplitude, math.floor(display_interval_ms), song_name)

    #TODO make these variables instead of being hardcoded
    screenL = 1920
    screenH = 1080

    create_new_ellipse_profile(song_name=song_name, vocal_amplitude = vocal_amplitude,
                                              other_amplitude=other_amplitude, screenL=screenL, screenH=screenH,animation_frames=animation_frames)

    create_new_beat_tempo_profile(song_path, song_name)
    # create_new_other_profile(other_amplitude,rate_other,song_path,song_name)

def run(song_path):
    stem_dir = '5stems'
    song_name = os.path.basename(song_path)

    screenL = 1920
    screenH = 1080

    vocal_file = os.path.join('SpleeterOutputs_16-bit',
                              stem_dir,
                              song_name + "_vocals_16-bit.wav")

    other_file = os.path.join('SpleeterOutputs_16-bit',
                              stem_dir,
                              song_name + "_other_16-bit.wav")

    rate, vocal_amplitude = read(vocal_file)
    rate_other, other_amplitude = read(other_file)

    num_samples = len(vocal_amplitude)

    animation_frames = []

    for i in range(math.floor((num_samples * animation_fps) / 44100)):
        animation_frames.append(int(i * 44100 / animation_fps))

    # print("these are the frames to animate on:")
    # print(animation_frames)

    # try:
    #
    #     pickle_in = open("pickles/" + song_name + "_vocal.pickle", "rb")
    #     crepe_stuff = pickle.load(pickle_in)
    #     crepe_vocal_time, crepe_vocal_frequency, crepe_vocal_confidence, crepe_vocal_activation = \
    #         crepe_stuff[0], crepe_stuff[1], crepe_stuff[2], crepe_stuff[3]
    #
    # except:
    #
    #     # Crepe returns vocal fundemental frequency info
    #     crepe_vocal_time, crepe_vocal_frequency, crepe_vocal_confidence, crepe_vocal_activation = \
    #         create_new_vocal_profile(rate, vocal_amplitude, display_interval_ms, song_name)
    #

    try:
        pickle_in = open("pickles/" + song_name + "_beats.pickle", "rb")
        beat_times, tempo = pickle.load(pickle_in)

    except:
        beat_times, tempo = create_new_beat_tempo_profile(song_path, song_name)

    # try:
    #     pickle_in = open("pickles/" + song_name + "_other.pickle", "rb")
    #     pitches,magnitudes = pickle.load(pickle_in)
    #
    # except:
    #     pitches,magnitudes = create_new_other_profile(other_amplitude,rate_other,song_path, song_name,display_interval_ms)

    try:
        print("opening ellipses pickle")
        pickle_in = open("pickles/" + song_name + "_ellipses.pickle", "rb")
        ellipses = pickle.load(pickle_in)

    except:
        print("couldnt open ellipses pickle")
        ellipses = create_new_ellipse_profile(song_name=song_name, vocal_amplitude = vocal_amplitude,
                                              other_amplitude=other_amplitude, screenL=screenL, screenH=screenH,animation_frames=animation_frames)

    # def detect_pitch(y, sr, t):
    #     index = magnitudes[:, t].argmax()
    #     pitch = pitches[index, t]
    #
    #     return pitch
    #
    # other_pitches = []
    #
    # for i in range(len(pitches)):
    #     # print(detect_pitch(pitches,44100,i))
    #     other_pitches.append(detect_pitch(pitches,44100,i))

    print("estimated tempo", tempo)
    print("len amplitude before frame skip", len(vocal_amplitude))

    # print("len other pitches",len(other_pitches))
    #
    # print("len crepe",len(crepe_vocal_confidence))

    pygame.init()

    clock = pygame.time.Clock()
    # screen = pygame.display.set_mode([width, height])
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = pygame.display.get_surface().get_size()

    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.mixer.init()
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()
    now = time.time()

    # def remove_confidence_outliers(confidence):
    #
    #     return scipy.signal.medfilt(confidence)
    #
    # crepe_vocal_confidence = remove_confidence_outliers(crepe_vocal_confidence)

    # max_frequency = max(crepe_vocal_frequency)

    # from math import log2, pow
    # ##https: // www.johndcook.com / blog / 2016 / 02 / 10 / musical - pitch - notation /
    #
    # #############
    # def pitch(freq):
    #     A4 = 440
    #     C0 = A4 * pow(2, -4.75)
    #     pitch_names =  ["C" ,"C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    #
    #     h = round(12 * log2(freq / C0))
    #     octave = h // 12
    #     n = h % 12
    #     return pitch_names[n] + str(octave)

    #############

    # def display_vocals(index):
    #     if crepe_vocal_confidence[index] > 0.75:
    #         # color = [255 * crepe_vocal_frequency[i]/max_frequency,255 * crepe_vocal_frequency[i]/max_frequency ,255 * crepe_vocal_frequency[i]/max_frequency]
    #         color = [200, 100, 255]
    #
    #         note_frequency = crepe_vocal_frequency[index]
    #
    #         # print(note_frequency)
    #
    #         pygame.draw.circle(screen,
    #                            color,
    #                            (int(width / 2), int((3 * height / 4) - note_frequency)),
    #                            50,
    #                            0)
    #
    #         font = pygame.font.SysFont('Calibri',35,True,True)
    #         text = font.render(pitch(note_frequency),True,(255,255,255))
    #         screen.blit(text,[100,240])



    color = [255,255,255]


    fullscreen_display = True
    music_paused = False

    beat_times_index = 0

    animation_frame_index = 0

    colors = [[255, 100,100],[255, 190, 100], [255, 127, 100], [255, 190, 100],[200, 200, 100],[127, 255, 100],
              [100, 255, 100],[100, 127, 127],[100, 100, 255], [23, 21, 175],[46, 43, 95],[90, 21, 75], [139, 100, 255],[200, 100, 127]]

    done = False

    for i in range(len(animation_frames)):
        animation_frames[i] = animation_frames[i] / 44100

    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("got pygame.quit")
                done = True
                pygame.quit()
                sys.exit()

            #This should update the params so the animations work for any size screen. Doesn't work right now.
            if event.type == pygame.VIDEORESIZE:
                width, height = pygame.display.get_surface().get_size()

        keys_pressed = pygame.key.get_pressed()
        if (keys_pressed[pygame.K_RSHIFT] or keys_pressed[pygame.K_LSHIFT]) and(keys_pressed[pygame.K_TAB]):

            if fullscreen_display:
                pygame.display.set_mode((0,0),pygame.RESIZABLE)
                fullscreen_display = False

            else:
                pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                fullscreen_display = True

        if keys_pressed[pygame.K_SPACE]:
            print("space bar pressed")

            if music_paused:
                pygame.mixer.music.unpause()
                music_paused = not music_paused
            else:
                pygame.mixer.music.pause()
                music_paused = not music_paused

            pygame.time.wait(500)

        pygame.event.get()

        player_time = pygame.mixer.music.get_pos()/1000

        if beat_times[beat_times_index] < player_time + 0.05:

            screen.fill(colors[beat_times_index % len(colors)])

            beat_times_index += 1

        while animation_frames[animation_frame_index] < player_time:

            for shape in ellipses[animation_frame_index]:
                pygame.draw.lines(screen, color, True, shape,4)

            animation_frame_index +=1

        clock.tick(animation_fps - 1)

        pygame.display.update()

