import numpy as np
from scipy.misc import imread, imresize


def preprocess_input(x, v2=True):
	'''function to convert image array into float-32 bit array'''
	x = x.astype('float32')
	x = x / 255.0
	if v2:
		x = x - 0.5
		x = x * 2.0
	return x

def _imread(image_name):
    ''' function to load image array'''
    return imread(image_name)

def _imresize(image_array, size):
	''' function to resize the image array'''
	return imresize(image_array, size)

def to_categorical(integer_classes, num_classes=2):
    integer_classes = np.asarray(integer_classes, dtype='int')
    num_samples = integer_classes.shape[0]
    categorical = np.zeros((num_samples, num_classes))
    categorical[np.arange(num_samples), integer_classes] = 1
    return categorical

