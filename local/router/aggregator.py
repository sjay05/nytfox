import cv2
import imagezmq
import time
import zmq

image_hub = imagezmq.ImageHub(open_port = 'tcp://*:6666')

stream_monitor = imagezmq.ImageSender(connect_to = 'tcp://*:5577', REQ_REP = False)

def main():
  print("[LOG] Waiting for camera...")
  first_recv = False
  while True:
    rpi_name, image = image_hub.recv_image()
    if first_recv == False:
      print("[LOG] Connected - First Frame Received")
      first_recv = True
    image_hub.send_reply(b"OK");
    stream_monitor.send_image(rpi_name, image)

if __name__ == "__main__":
  main()