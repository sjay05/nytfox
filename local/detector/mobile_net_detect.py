import numpy as np
import cv2
import time

class MobileNet_Detector:
  def __init__(self):
    classPath = 'mobilenet/coco.names'
    self.labels = []
    with open(classPath, 'rt') as f:
      self.labels = f.read().rstrip('\n').split('\n')
    print(f"[INFO] coco.names loaded with {len(self.labels)} classes.")
    
    configPath = 'mobilenet/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    weightsPath = 'mobilenet/frozen_inference_graph.pb'

    print("[INFO] Loading DNN from disk...")
    self.net = cv2.dnn_DetectionModel(weightsPath,configPath)
    self.net.setInputSize(320, 320)
    self.net.setInputScale(1.0 / 127.5)
    self.net.setInputMean((127.5, 127.5, 127.5))
    self.net.setInputSwapRB(True)

    self.thres = 0.5
    self.nms_thres = 0.5
    self.previous = time.time()

    
  def DetectFrame(self, img):
      allID, conf, bbox = self.net.detect(img, confThreshold = self.thres)
      bbox = list(bbox)
      conf = list(np.array(conf).reshape(1, -1)[0])
      conf = list(map(float, conf))

      vehicles = ['train', 'truck', 'boat', 'bicycle', 'motorbike', 'car', 'bus', 'sports ball', 'suitcase']

      start = time.time()
      indices = cv2.dnn.NMSBoxes(bbox, conf, self.thres, self.nms_thres)
      all_boxes = []
      end = time.time()

      for index in indices:
        ci = index[0]
        box = bbox[ci]
        x, y = box[0], box[1]
        w, h = box[2], box[3]
        
        if (allID[ci][0] - 1 > len(self.labels)):
          continue

        current_time = time.time()

        final_name = ""
        if self.labels[allID[ci][0] - 1] in vehicles:
          if (self.labels[allID[ci][0] - 1] != "car"):
            print(f"[WARNING] Assumed {self.labels[allID[ci][0] - 1]} for car.")
          final_name = "car"  
        
        if self.labels[allID[ci][0] - 1] == 'person':
          if (float(current_time - self.previous) > 1.0):
            print("[LOG] DNN Detected Person in {:.6f} seconds".format(end - start)) 
            self.previous = current_time

          final_name = "person"

        if final_name != "car" and final_name != "person":
          continue

        all_boxes.append((final_name, x, y, x + w, y + h))

      return all_boxes