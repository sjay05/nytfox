from logging import Logger
from flask import Flask, render_template, Response, request
import cv2
import imagezmq
import imutils
from flask_socketio import SocketIO
import logging

app = Flask(__name__)
socketio = SocketIO(app)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def gen_frames():
  image_hub = imagezmq.ImageHub(open_port='tcp://localhost:5577', REQ_REP=False)
  while True:
    rpi_name, frame = image_hub.recv_image()
    ret, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    yield (b'--frame\r\n'
      b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/video_feed')
def video_feed():
  return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stream')
def stream():
  return render_template('tmp_stream.html')

@socketio.on('connect', namespace='/theft_alert')
def connect_camera():
  print('[INFO] Image detector client connected: {}'.format(request.sid))

@socketio.on('disconnect', namespace='/theft_alert')
def disconnect_camera():
    print('[INFO] Image detector client disconnected: {}'.format(request.sid))

@socketio.on('od2cloud')
def handle_cv_message(message):
  socketio.emit('cloud2client', message, namespace='/web')

@app.route('/')
def index():
  return render_template('tmp_index.html')

if __name__ == '__main__':
#  app.run(debug = True)
  app.run(host="0.0.0.0")
