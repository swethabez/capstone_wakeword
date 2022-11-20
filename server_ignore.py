# Import libraries
import numpy as np
import sounddevice as sd
import wavio as wv

from flask import Flask, request, jsonify, render_template
import librosa
from joblib import load

# load the pipeline object
fname = '/models/LSTM_Spotify.sav'
#pipeline = load(open(fname))

def featuresExtractor(file):
    audio, sample_rate = librosa.load(file, res_type='kaiser_fast')
    #set a window width to 25 ms and the stride to 10 ms
    mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40,hop_length=int(0.010*sample_rate), n_fft=int(0.025*sample_rate))
    mfccs_scaled_features = np.mean(mfccs_features.T,axis=0)
    return mfccs_scaled_features

def requestResults(name):
    data = featuresExtractor(name)
    result = pipeline.predict(data)

    return result

freq = 44100
duration = 8
# start flask
app = Flask(__name__)

# render default webpage
@app.route('/')
def home():
    return render_template('index3.html')

# when the post method detect, then redirect to success function
@app.route('/', methods=['POST', 'GET'])
def get_data():
    if request.method == 'POST':
        if request.form.get('action1') == 'Record':
            filename = "test.wav"
            recording = sd.rec(int(duration * freq), samplerate=freq, channels=1)

            # Record audio for the given number of seconds
            sd.wait()

            wv.write(filename, recording, freq, sampwidth=2)

        else:
            pass  # unknown
    elif request.method == 'GET':
        return render_template('index3.html', form=form)

    return render_template("index3.html")

# get the data for the requested query
@app.route('/model', methods=['GET', 'POST'])
def model():
    res = ['No Wake Word', 'Yes! Correct']
    if request.method == "POST":
        models = request.form.get("models", None)

        result = requestResults('test.wav')
        r1 = res[int(result)]

        return render_template("index3.html", r1=r1, models=models)



if __name__ == '__main__':
    app.run()