#!/usr/bin/env python2.7
import argparse
import os
import numpy
import glob
import utils.audioTrainTest as aT

def trainClassifierWrapper(method, beatFeatures, directories, modelName):
    '''function to get user inputs'''
    
    if len(directories) < 2:
        raise Exception("At least 2 directories are needed")
    aT.featureAndTrain(directories, 1, 1, aT.shortTermWindow, aT.shortTermStep,
                       method.lower(), modelName, computeBEAT=beatFeatures)

def classifyFileWrapper(inputFile, modelType, modelName):
    ''' function to classify a single file '''
    
    if not os.path.isfile(modelName):
        raise Exception("Input modelName not found!")
    if not os.path.isfile(inputFile):
        raise Exception("Input audio file not found!")

    [Result, P, classNames] = aT.fileClassification(inputFile, modelName,
                                                    modelType)
    print "{0:s}\t{1:s}".format("Class", "Probability")               # print each genre and probability for each file

    for i, c in enumerate(classNames):
        print "{0:s}\t{1:.2f}".format(c, P[i])                       # print genre and probability till 2 decimal precision

    print "Winner class: " + classNames[int(Result)]                 # print the winner genre and its probability

def classifyFolderWrapper(inputFolder, modelType, modelName, outputMode=False):
    ''' function to classify a whole folder'''

    if not os.path.isfile(modelName):
        raise Exception("Input modelName not found!")

    types = ('*.wav', '*.mp3')                              # acceptable file types

    wavFilesList = []                                      # empty list for listing all files

    for files in types:
        wavFilesList.extend(glob.glob(os.path.join(inputFolder, files)))             # glob to have same paths as unix file sysytem

    wavFilesList = sorted(wavFilesList)                       # sorting the  file list

    if len(wavFilesList) == 0:
        print "No WAV files found!"
        return

    Results = []                           # empty result list

    newDict = dict()                        # empty dictionary to save file path and genre

    for wavFile in wavFilesList:
        [Result, P, classNames] = aT.fileClassification(wavFile, modelName,
                                                        modelType)
        Result = int(Result)
        Results.append(Result)
        if outputMode:
            print "{0:s}\t{1:s}".format(wavFile, classNames[Result])
            newDict.update({wavFile:classNames[Result]})                  # updating dictionary with each file path and genre
    Results = numpy.array(Results)
    print(newDict)
   

    # print distribution of classes:
    [Histogram, _] = numpy.histogram(Results,
                                     bins=numpy.arange(len(classNames) + 1))
    for i, h in enumerate(Histogram):
        print "{0:20s}\t\t{1:d}".format(classNames[i], h)

def parse_arguments():
    ''' function to take user argument help'''

    parser = argparse.ArgumentParser(description="pyAudioAnalysis classification")

    tasks = parser.add_subparsers(
        title="subcommands", description="available tasks",
        dest="task", metavar="")

    trainClass = tasks.add_parser("trainClassifier",
                                  help="Train an SVM or KNN classifier")
    trainClass.add_argument("-i", "--input", nargs="+",
                            required=True, help="Input directories")
    trainClass.add_argument("--method",
                            choices=["svm", "gradientboosting"],
                            required=True, help="Classifier type")
    trainClass.add_argument("--beat", action="store_true",
                            help="Compute beat features")
    trainClass.add_argument("-o", "--output", required=True,
                            help="Generated classifier filename")

    classFile = tasks.add_parser("classifyFile",
                                 help="Classify a file using an "
                                      "existing classifier")
    classFile.add_argument("-i", "--input", required=True,
                           help="Input audio file")
    classFile.add_argument("--model", choices=["svm", "gradientboosting"],
                           required=True, help="Classifier model")
    classFile.add_argument("--classifier", required=True,
                           help="Classifier to use (path)")

    classFolder = tasks.add_parser("classifyFolder")
    classFolder.add_argument("-i", "--input", required=True,
                             help="Input folder")
    classFolder.add_argument("--model", choices=["svm", "gradientboosting"],
                             required=True, help="Classifier type")
    classFolder.add_argument("--classifier", required=True,
                             help="Classifier to use (filename)")
    classFolder.add_argument("--details", action="store_true",
                             help="Plot details (otherwise only "
                                  "counts per class are shown)")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    if args.task == "trainClassifier":
        # Train classifier from data (organized in folders)
        trainClassifierWrapper(args.method, args.beat, args.input, args.output)
    elif args.task == "classifyFile":
        # Apply audio classifier on audio file
        classifyFileWrapper(args.input, args.model, args.classifier)
    elif args.task == "classifyFolder":
        # Classify every WAV file in a given path
        classifyFolderWrapper(args.input, args.model, args.classifier,
                              args.details)
