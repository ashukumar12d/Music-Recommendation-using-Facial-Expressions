#
import os
import subprocess
import ast
import utils.utilities as util
import random

# get the address of dictionary from the audioanalysis and import function namespace
dictStr = os.popen(
    'bash -c "python audioAnalysis.py classifyFolder -i /mnt/e/test5/ --model svm --classifier models/svmGenreRecog '
    '--details | tee /dev/stderr | grep {*}"').read()

dictdict = ast.literal_eval(dictStr)      # use abstract syntax of the dictionary safely

import emotions # import *        # import the namespace module of the emotion.py

emotion_mode = emotions.emotion_mode

print("\nChoosing a song for "+ emotion_mode + " mood")              # print the value of emotion_mode from emotions.py

songs = []                          # empty list for songs path

for song, genre in dictdict.items():          # iterate in the dictionary containing songs and their paths
    if emotion_mode == "neutral":
        #if genre == "rock" or genre == "metal":
        songs.append(song)

    elif emotion_mode == "sad":
        if genre == "blues" or genre == "jazz" or genre == "classical" or genre == "country":
            songs.append(song)

    elif emotion_mode == "happy":
        if genre == "rock" or genre == "metal" or genre == "pop":
            songs.append(song)

    elif emotion_mode == "angry":
        if genre == "metal" or genre == "rock":
            songs.append(song)

    elif emotion_mode == "surprised":
        if genre == "hiphop" or genre == "disco":
            songs.append(song)

    elif emotion_mode == "disgust":
        if genre == "raggae" or genre == "metal" or genre == "rock":
            songs.append(song)

try:
    finalPath = util.changeToWindows(random.choice(songs))              # randomly choose the song and pass the path for playing
    print('\nPlaying ' + finalPath)
    util.playMedia(finalPath)                                # play the song
except IndexError:
    print("\numm... no song for this mood... ):")
