import numpy as np
import cv2

from mobile_net_detect import MobileNet_Detector

# from face_recog import FaceRecognition

def Mid(xa, ya, xb, yb):
  return ((xa + xb) / 2.0, (ya + yb) / 2.0)

def Dist(xa, ya, xb, yb):
  return (xa - xb) * (xa - xb) + (ya - yb) * (ya - yb)

def ProcessFrame(img, det):
  result = det.DetectFrame(img)

  height, width = img.shape[:2]

  cars, people = [], []
  for tup in result:
    name, xa, ya, xb, yb = tup

    if name == 'car' and (abs(xa - xb) < width / 4 or abs(ya - yb) < height / 4):
      continue

    if name == "car":
      cars.append([xa, ya, xb, yb])
    else:
      people.append([xa, ya, xb, yb])

    cv2.rectangle(img, (xa, ya), (xb, yb), color = (0, 255, 0), thickness = 2)
    cv2.putText(img, name, (xa, ya - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

#  FaceRecognition(img)

  if len(cars) == 0 or len(people) == 0:
    return False

  closest = 1e18
  theft_tuple = []

  for car in cars:
    for person in people:
      p_mid = Mid(person[0], person[1], person[2], person[3])
      mn_dist = 1e18
      mn_dist = min(mn_dist, Dist(car[0], car[1], p_mid[0], p_mid[1]));
      mn_dist = min(mn_dist, Dist(car[0], car[3], p_mid[0], p_mid[1]));
      mn_dist = min(mn_dist, Dist(car[0], (car[1] + car[3]) / 2, p_mid[0], p_mid[1]));
      mn_dist = min(mn_dist, Dist(car[2], car[3], p_mid[0], p_mid[1]));
      mn_dist = min(mn_dist, Dist(car[2], car[1], p_mid[0], p_mid[1]));
      mn_dist = min(mn_dist, Dist(car[2], (car[3] + car[1]) / 2, p_mid[0], p_mid[1]));
      if mn_dist < closest:
        closest = mn_dist
        theft_tuple = (car, person)

  car_p, p_p = theft_tuple
  cv2.rectangle(img, (car_p[0], car_p[1]), (car_p[2], car_p[3]), color = (0, 0, 255), thickness = 2)
  cv2.putText(img, "car", (car_p[0], car_p[1] - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

  cv2.rectangle(img, (p_p[0], p_p[1]), (p_p[2], p_p[3]), color = (0, 0, 255), thickness = 2)
  cv2.putText(img, "person", (p_p[0], p_p[1] - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

  car_mid = Mid(car_p[0], car_p[1], car_p[2], car_p[3])
  p_mid = Mid(p_p[0], p_p[1], p_p[2], p_p[3])

  return True

det = MobileNet_Detector()

def TheftProcessFrame(img):
  return ProcessFrame(img, det) 
  cv2.waitKey(1)

"""
def Test():
  cap = cv2.VideoCapture('test_run.mov')
  cap = cv2.VideoCapture(0)
  while True:
    res, img = cap.read()
    ProcessFrame(img, det)
    cv2.imshow('Output', img)
    cv2.waitKey(1)

Test()
"""