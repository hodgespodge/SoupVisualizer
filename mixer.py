

import os.path, sys
import pygame.mixer, pygame.time
mixer = pygame.mixer
time = pygame.time

# main_dir = os.path.split(os.path.abspath(__file__))[0]

stem_dir = '5stems'
song = 'No Surprises'
instrument = 'bass'

song_instrument = song + "_" + instrument + ".wav"

def main(file_path=None):
    """Play an audio file as a buffered sound sample
    Option argument:
        the name of an audio file (default data/secosmic_low.wav
    """
    if file_path is None:
        # file_path = os.path.join(main_dir,
        #                          'data',
        #                          'secosmic_lo.wav')

        file_path = os.path.join('SpleeterOutputs',
                                 stem_dir,
                                 song_instrument)

    #choose a desired audio format
    mixer.init(44100) #raises exception on fail


    print(file_path)

    #load the sound    
    sound = mixer.Sound(file_path)


    #start playing
    print ('Playing Sound...')
    channel = sound.play()


    #poll until finished
    while channel.get_busy(): #still playing
        print ('  ...still going...')
        time.wait(1000)
    print ('...Finished')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()