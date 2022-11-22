from flask import Flask
from flask import request
from flask import render_template
import os
import numpy as np
import librosa
#import joblib
import tensorflow as tf
from tensorflow import keras
import wavio as wv
#from scipy.io import wavfile
import soundfile as sf


app = Flask(__name__)

# load the pipeline object
base_filename = 'LSTM_Spotify'
#dir_name='/Users/sbezawada/Documents/Workspace/MLE-COURSE/Capstone2/capstone_wakeword/app/models/'
dir_name = './models/'
suffix='.sav'
file = os.path.join(dir_name, base_filename + suffix)
file2 = os.path.join(dir_name, base_filename)
#pipeline = joblib.load(open(file,'rb'))
pipeline = keras.models.load_model(file2)

def featuresExtractor(file):
    audio, sample_rate = librosa.load(file, res_type='kaiser_fast')
    print(sample_rate)
    #set a window width to 25 ms and the stride to 10 ms
    mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40,hop_length=int(0.010*sample_rate), n_fft=int(0.025*sample_rate))
    mfccs_scaled_features = np.mean(mfccs_features.T,axis=0)
    return mfccs_scaled_features

def requestResults(name):
    data = featuresExtractor(name)
    print(data)
    data= np.array(data.tolist())
    data = data.reshape(1,1,data.shape[0])
    print(data.shape)
    result = pipeline.predict(data)
    print(result)
    return result

freq = 44100
duration = 8
name='test'

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        f = request.files['audio_data']
        with open('audio.wav', 'wb') as audio:
            f.save(audio)

        print('file uploaded successfully')
        #samplerate, data = wavfile.read('audio.wav')
        data, fs = sf.read('audio.wav')
        print(data.min(),data.max())
        wv.write(name + ".wav", data, freq, sampwidth=2) #score of .34
        #wv.write(name + ".wav", data, freq, sampwidth=2,scale=1) #error: TypeError: cannot unpack non-iterable int object

        return render_template('index.html', request="POST")
    else:
        return render_template("index.html")


@app.route('/model', methods=['GET', 'POST'])
def model():
    res = ['No Wake Word', 'Hi! Whats up!']
    if request.method == "POST":
        models = request.form.get("models", None)
        result = requestResults('test.wav')
        result = (result > 0.3).astype('int')
        r1 = res[int(result)]

        return render_template("index.html", r1=r1, models=models)


if __name__ == "__main__":
    app.run(debug=True,  port=5000)