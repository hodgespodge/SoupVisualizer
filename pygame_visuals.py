from scipy.io.wavfile import read

import pygame, sys, time, os
from PreprocessingFunctions import *
import pickle
import math

animation_fps = 30

display_interval_ms = 1000 / animation_fps
display_interval_s = display_interval_ms / 1000

def create_instrument_charactaristics(song_path,num_points,screen_resolution):

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

    create_new_ellipse_profile(song_name=song_name, vocal_amplitude = vocal_amplitude, other_amplitude=other_amplitude,
                               screenL=screen_resolution[0], screenH=screen_resolution[1],
                               animation_frames=animation_frames,num_points=num_points)

    create_new_beat_tempo_profile(song_path, song_name)

def run(song_path,num_points,screen_resolution):
    stem_dir = '5stems'
    song_name = os.path.basename(song_path)


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

    try:
        pickle_in = open("pickles/" + song_name + "_beats.pickle", "rb")
        beat_times, tempo = pickle.load(pickle_in)

    except:
        beat_times, tempo = create_new_beat_tempo_profile(song_path, song_name)

    try:
        print("opening ellipses pickle")
        pickle_in = open("pickles/" + song_name + "_ellipses.pickle", "rb")
        ellipses = pickle.load(pickle_in)

    except:
        print("couldnt open ellipses pickle")
        ellipses = create_new_ellipse_profile(song_name=song_name, vocal_amplitude = vocal_amplitude,
                                              other_amplitude=other_amplitude, screenL=screen_resolution[0], screenH=screen_resolution[1],animation_frames=animation_frames,num_points=num_points)

    print("estimated tempo", tempo)
    print("len amplitude before frame skip", len(vocal_amplitude))

    pygame.init()

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = pygame.display.get_surface().get_size()

    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.mixer.init()
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()
    now = time.time()

    line_color = [255,255,255]

    fullscreen_display = True
    music_paused = False

    beat_times_index = 0

    animation_frame_index = 0

    background_colors = [[255, 100,100],[255, 190, 100], [255, 127, 100], [255, 190, 100],[200, 200, 100],[127, 255, 100],
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

            screen.fill(background_colors[beat_times_index % len(background_colors)])

            beat_times_index += 1

        while animation_frames[animation_frame_index] < player_time:

            for shape in ellipses[animation_frame_index]:
                pygame.draw.lines(screen, line_color, True, shape,4)

            animation_frame_index +=1

        clock.tick(animation_fps - 1)

        pygame.display.update()

pygame.quit()