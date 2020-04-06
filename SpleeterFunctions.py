from scipy.io import wavfile
from spleeter.separator import Separator
import numpy as np
import warnings
import wavio
import os
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
