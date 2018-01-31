import os, glob, eyed3, ntpath, shutil, numpy
import scipy.io.wavfile as wavfile
import pydub
from pydub import AudioSegment

def readAudioFile(path):
    '''
    This function returns a numpy array that stores the audio samples of a specified wav file
    '''
    extension = os.path.splitext(path)[1]

    try:
        if extension.lower() == '.mp3' or extension.lower() == '.wav' or extension.lower() == '.au':            
            try:
                audiofile = AudioSegment.from_file(path)
            except:
                print "Error: file not found or other I/O error. (DECODING FAILED)"
                return (-1,-1)                

            if audiofile.sample_width==2:                
                data = numpy.fromstring(audiofile._data, numpy.int16)
            elif audiofile.sample_width==4:
                data = numpy.fromstring(audiofile._data, numpy.int32)
            else:
                return (-1, -1)
            Fs = audiofile.frame_rate
            x = []
            for chn in xrange(audiofile.channels):
                x.append(data[chn::audiofile.channels])
            x = numpy.array(x).T
        else:
            print "Error in readAudioFile(): Unknown file type!"
            return (-1,-1)
    except IOError: 
        print "Error: file not found or other I/O error."
        return (-1,-1)

    if x.ndim==2:
        if x.shape[1]==1:
            x = x.flatten()

    return (Fs, x)

def stereo2mono(x):
	

    if x.ndim==1:
        return x
    elif x.ndim==2:
        if x.shape[1]==1:
            return x.flatten()
        else:
            if x.shape[1]==2:
                #return ( (x[:,1] / 2) + (x[:,0] / 2) )
				return x.sum(axis=1) / 2
            else:
                return -1

