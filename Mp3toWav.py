from os import path
import sys
from pydub import AudioSegment

# files

src = sys.argv[1]
dst = sys.argv[1][:-3]+"wav"

# src = "transcript.mp3"
# dst = "test.wav"

# convert wav to mp3
sound = AudioSegment.from_mp3(src)
sound.export(dst, format="wav")