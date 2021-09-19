import numpy as np
import cv2

class Yolo_Detector:
  def __init__(self):
    classPath = 'yolo/coco.names'
    self.labels = []
    with open(classPath, 'rt') as f:
      self.labels = f.read().strip().split('\n')

    weightPath = 'yolo/yolov3.weights'
    configPath = 'yolo/yolov3.cfg'

    self.net = cv2.dnn.readNetFromDarknet(configPath, weightPath)

  def DetectFrame(self, img):
    vehicles = ['truck', 'car', 'train']
    height, width = img.shape[:2]
    ln = self.net.getLayerNames()
    ln = [ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    self.net.setInput(blob)
    layerOutputs = self.net.forward(ln)

    boxes, conf, classIDs = [], [], []

    for output in layerOutputs:
      for detection in output:
        scores = detection[5:]
        classID = np.argmax(scores)
        confidence = scores[classID]

        if confidence > 0.1:
          box = detection[0:4] * np.array([width, height, width, height])
          center_x = int(box[0])
          center_y = int(box[1])
          b_width = int(box[2])
          b_height = int(box[3])

          x = int(center_x - (b_width / 2))
          y = int(center_y - (b_height / 2))

          boxes.append([x, y, int(b_width), int(b_height)])
          conf.append((float(confidence)))
          classIDs.append(classID)

    indexes = cv2.dnn.NMSBoxes(boxes, conf, 0.5, 0.3)
    all_boxes = []

    if len(indexes) > 0:
      for i in indexes.flatten():
        (x, y) = (boxes[i][0], boxes[i][1])
        (w, h) = (boxes[i][2], boxes[i][3]) 
        if self.labels[classIDs[i]] in vehicles:
          all_boxes.append(('car', x, y, x + w, y + h))
        if self.labels[classIDs[i]] == 'person':
          all_boxes.append(('person', x, y, x + w, y + h))        

#    print(all_boxes)
    return all_boxes
