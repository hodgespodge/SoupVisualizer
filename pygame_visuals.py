from scipy.io.wavfile import read
from random import randint
from numpy import fft
import pygame, sys, time, os
from PreprocessingFunctions import *
import crepe
import scipy.signal


stem_dir = '5stems'
song = 'Creep'
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
    # graphic interface dimensions
    width, height = 840, 720
    center = [width // 2, height // 2]

    frame_rate = 44100

    rate, vocal_amplitude = read(vocal_file)
    rate2, drum_amplitude = read(drums_file)

    print(len(drum_amplitude))

    print("len amplitude before frame skip",len(vocal_amplitude))

    animation_fps = 15

    display_interval_ms = 1000/animation_fps
    display_interval_s = display_interval_ms/1000

    print(display_interval_ms)


    #Crepe returns vocal fundemental frequency info
    crepe_vocal_time, crepe_vocal_frequency, crepe_vocal_confidence, crepe_vocal_activation = get_crepe_confidence(vocal_amplitude, rate,step_size=display_interval_ms)

    frame_skip = 96
    vocal_amplitude = vocal_amplitude[:, 0] + vocal_amplitude[:, 1]
    vocal_amplitude = vocal_amplitude[::frame_skip]
    frequency = list(abs(fft.fft(vocal_amplitude)))

    # print("fundemental freq list",len(get_fundemental_frequency(file_name).selected_array['frequency']))

    # scale the amplitude to 1/4th of the frame height and translate it to height/2(central line)
    max_amplitude = max(vocal_amplitude)
    for i in range(len(vocal_amplitude)):
        vocal_amplitude[i] = float(vocal_amplitude[i]) / max_amplitude * height / 4 + height / 2
    vocal_amplitude = [int(height / 2)] * width + list(vocal_amplitude)

    while(True): #Wait for user to specify run
        play =  input()
        if play == "1":
            break

    pygame.init()
    screen = pygame.display.set_mode([width, height])

    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.mixer.init()
    pygame.mixer.music.load(song_file)
    pygame.mixer.music.play()
    now = time.time()

    def remove_confidence_outliers(confidence):

        return scipy.signal.medfilt(confidence)

    crepe_vocal_confidence = remove_confidence_outliers(crepe_vocal_confidence)

    max_frequency = max(crepe_vocal_frequency)

    def display_vocals(index):
        if crepe_vocal_confidence[index] > 0.75:
            # color = [255 * crepe_vocal_frequency[i]/max_frequency,255 * crepe_vocal_frequency[i]/max_frequency ,255 * crepe_vocal_frequency[i]/max_frequency]
            color = [200, 100, 255]

            pygame.draw.circle(screen,
                               color,
                               (int(width / 2), int((3 * height / 4) - crepe_vocal_frequency[index])),
                               50,
                               0)

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


    for i,t in enumerate(crepe_vocal_time):

        screen.fill([0, 0, 0])
        pygame.event.get()

        pos = pygame.mixer.music.get_pos()
        if pos/1000 > t:
            continue

        # try:

        display_vocals(index = i)
        display_drums()

        time.sleep(display_interval_s)

        pygame.display.update()
        # except:
        #     pass

if __name__ == '__main__':
    main()