from socket import socket
import cv2
import imagezmq
import time
import zmq
import datetime
import base64
import socketio

from theft_detect import TheftProcessFrame

sio = socketio.Client()

image_hub = imagezmq.ImageHub(open_port='tcp://localhost:5577', REQ_REP=False)

print("[LOG] Waiting for router...")
first_recv = False

def _convert_image_to_jpeg(image):
  # Encode frame as jpeg
  frame = cv2.imencode('.jpg', image)[1].tobytes()
  # Encode frame in base64 representation and remove
  frame = base64.b64encode(frame).decode('utf-8')
  return "data:image/jpeg;base64,{}".format(frame)

def send_alert(frame):
  text = f"Detected at {datetime.datetime.now()} <br><br> Objects: [Car, Person, Person]"
  sio.emit('od2cloud', {'text': text, 'image': _convert_image_to_jpeg(frame)})

if __name__ == '__main__':
  sio.connect('http://localhost:5000/theft_alert')
  while True:
    rpi_name, image = image_hub.recv_image()
    if first_recv == False:
      print("[LOG] Connected - First Frame Received")
      first_recv = True
    
    prev_image = image
    theft_flag = TheftProcessFrame(image)    
    if theft_flag:
      send_alert(prev_image)