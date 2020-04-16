from scipy.io import wavfile
from spleeter.separator import Separator
import numpy as np
import warnings
import wavio
import os
from pydub import AudioSegment
def spleet_wav(songpath,outfolder,num_stems):

    rate, audio = wavfile.read(songpath)
    songname = os.path.basename(os.path.normpath(songpath))

    warnings.filterwarnings('ignore')

    stem_param = str(num_stems) + 'stems'

    # Using embedded configuration... stems can be 2,4, 5 (number of instruments in network)
    separator = Separator('spleeter:'+stem_param)

    # Perform the separation
    prediction = separator.separate(audio)

    rate = 44100

    for instrument in prediction:

        name = outfolder + "/" + songname + "_" + instrument + "_16-bit.wav"

        print("Saving", instrument, "as: ", name)

        wavio.write(name, prediction[instrument].astype(np.int16), rate, sampwidth=2)

    print("Overwriting other.wav with merged version")

    sound1 = AudioSegment.from_wav(outfolder + "/" + songname + "_" + "piano" + "_16-bit.wav")
    sound2 = AudioSegment.from_wav(outfolder + "/" + songname + "_" + "other" + "_16-bit.wav")

    merged_piano_other = sound1.overlay(sound2)

    merged_piano_other.export(outfolder + "/" + songname + "_" + "other" + "_16-bit.wav",format="wav")

    os.remove(outfolder + "/" + songname + "_" + "piano" + "_16-bit.wav")

    print("done merging other and piano")

def all_song_processing(fileName,split_wav_16_output,wav_16_output):

    import pygame_visuals

    try:
        os.remove(wav_16_output)
    except:
        pass

    spleet_wav(fileName, split_wav_16_output, 5)
    pygame_visuals.create_16_bit_wav(fileName, wav_16_output)
    pygame_visuals.create_instrument_charactaristics(fileName)