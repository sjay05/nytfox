import face_recognition
import numpy as np
import cv2

friendly_face = face_recognition.load_image_file("faces/Sanjay.jpeg")
friendly_encoding = face_recognition.face_encodings(friendly_face)[0]

known_face_encodings = [
  friendly_encoding
]
known_face_names = [
  "Sanjay"
]

def FaceRecognition(img):
  small_img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
  rgb_small_img = small_img[:, :, ::-1]

  face_locations = face_recognition.face_locations(rgb_small_img)
  face_encodings = face_recognition.face_encodings(rgb_small_img, face_locations)

  face_names = []

  if len(face_encodings) == 0:
    return False

  for face_encoding in face_encodings:
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    name = "Unknown"
    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    best_match_index = np.argmin(face_distances)
    if matches[best_match_index]:
      name = known_face_names[best_match_index]

    if name != "Unknown":
      face_names.append(name)

  for (top, right, bottom, left), name in zip(face_locations, face_names):
    # Scale back up face locations since the img we detected in was scaled to 1/4 size
    top *= 4
    right *= 4
    bottom *= 4
    left *= 4

    # Draw a box around the face
    cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)

    # Draw a label with a name below the face
    cv2.rectangle(img, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(img, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)