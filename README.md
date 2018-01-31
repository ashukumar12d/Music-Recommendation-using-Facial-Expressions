# Music-Recommendation-using-Facial-Expressions
An application which detects our emotions at real time using webcam feed and  smartly classifies your playlist into genres, at last playing a song that suits the mood specified by the facial analysis.
The application provides a pre-trained model for emotion or mood recognition which has been trained on Kaggle's 'Fer2013' dataset.
It also provides a pre-trained model for music classification which has been trained on GTZAN Genre collection.

For running emotion recognition only the file "emotions.py" can be run which takes input from the webcam feed.
The source can be changed in the code.

For running the music genre classification the file "audioAnalysis.p can be run with a full command like:-
                           'python audioAnalysis.py classifyFolder -i<inputfolder> --model <model_name> --classifier <location> --details'

instead of folder name a file name can also be given for classification by changing the argument 'classifyFolder' to 'classifyFile'.
As for the model it only supports 'svm' or 'gradient boosting', SVM beimng better.

To run the application as a whole 'special.py' is to be used and it will invoke emotional recognition. After you have a definite emotion 'q' is to be pressed to capture that emotion and play a suitable song.
This will make the emotion capture window exit.

![alt tag](https://user-images.githubusercontent.com/20767029/35637706-02c59806-06db-11e8-9bca-7b84cb4cc3e6.png)

