# ref. https://towardsdatascience.com/video-streaming-in-web-browsers-with-opencv-flask-93a38846fe00
from flask import Flask, render_template,Response
from datetime import datetime

import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0)

def gen_frame():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buff = cv2.imencode('.jpg', frame)
            frame = buff.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route("/video_feed")
def video_feed():
    return Response(gen_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/")
def home():    
    return render_template('index.html')

@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    clean_name = "Friend"
    content = "hi " + clean_name + " " + formatted_now

    return content

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
    #app.run()
