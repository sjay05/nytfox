from imutils.video import VideoStream
import imagezmq
import time
import socket
import cv2

sender = imagezmq.ImageSender(connect_to = "tcp://{}:6666".format("192.168.2.16"))

rpi_name = socket.gethostname()
cap = cv2.VideoCapture("rec.mov")

"""
1) Uncomment video to try with live stream (need a car in the frame).
2) Upload video and edit the file name to try detecting with recorded video.
"""

# video_stream = VideoStream(src = 0).start()

print(f"[INFO] - {rpi_name} video capture started...")

while True:
#  frame = video_stream.read();
  res, frame = cap.read()
  sender.send_image(rpi_name, frame)
  time.sleep(0.1)

video_stream.stop()
sender.close()
