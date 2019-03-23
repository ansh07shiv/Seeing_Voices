from flask import Flask, render_template, request, redirect
import speech_recognition as sr
import sys
import time
import moviepy.editor as mp
from werkzeug.utils import secure_filename
import subscene


app = Flask(__name__)

flag = 1
   
myList = []

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/record')
def record():
    r = sr.Recognizer()
    mic = sr.Microphone()
    t0 = time.time()
    while(True):
        print("Value of Flag ", flag)
        with mic as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
        try:
            print("In Try")
            rec = r.recognize_google(audio)
            mydict = {'time':round((time.time() - t0), 2), 'rec':rec}
            myList.append(mydict)
            print(rec)
            print(mydict)
            print(myList)
        except:      
            print("Error")
            break
    print(myList)
    return render_template("elements.html", results = myList)

@app.route('/stop')
def stop():
    return render_template("index1.html",results = myList)


@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    print("OK")
    file = request.files['file']
    filename = secure_filename(file.filename)
    print(filename)
    clip = mp.VideoFileClip(filename)
    clip.audio.write_audiofile("theaudio.wav")
    harvard = sr.AudioFile('theaudio.wav')
    r = sr.Recognizer()
    with harvard as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)
    msg = r.recognize_google(audio)

    return render_template("index1.html", results = msg)

@app.route('/subscene', methods = ['GET', 'POST'])
def subscene():
    url = "https://subscene.com/subtitles/title?q="
    url_add = request.form['film_name']
    vars_ = url_add.split(' ')
    ans = []
    for var in vars_:
        ans.append(var.lower())
        ans.append("+")
    ans[-1] = '&'
    ans.append("l")
    ans.append("=")
    string = ""
    string = string.join(ans)
    print(string.join(ans))
    return redirect(url+string)

if __name__ == '__main__':
    app.run(debug=True)