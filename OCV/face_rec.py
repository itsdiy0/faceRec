import os
from os import listdir
from os.path import isfile, join
import cv2 as cv
import numpy as np
import re 

haar_cascade = cv.CascadeClassifier('OCV/haar_face.xml')
DIR = 'static/uploads/train/'
global confidence,op_name
people = os.listdir(DIR)

def create_train():
    features = []
    labels = []
    for person in people:
        path = os.path.join(DIR, person)
        print(path)
        label = people.index(person)
        for img in os.listdir(path):
            img_path = os.path.join(path,img)
            img_array = cv.imread(img_path)
            if img_array is None:
                continue 
            gray = cv.cvtColor(img_array, cv.COLOR_BGR2GRAY)
            faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)
            for (x,y,w,h) in faces_rect:
                faces_roi = gray[y:y+h, x:x+w]
                features.append(faces_roi)
                labels.append(label)
    return features,labels

def create_recognizer():
    features,labels = create_train()
    features = np.array(features, dtype='object')
    labels = np.array(labels)
    face_recognizer = cv.face.LBPHFaceRecognizer_create()
    face_recognizer.train(features,labels)
    face_recognizer.save('face_trained.yml')

def recongnize():
    create_recognizer()
    face_recognizer = cv.face.LBPHFaceRecognizer_create()
    face_recognizer.read('face_trained.yml')    
    img = cv.imread("static/uploads/check_upload/uploaded.jpg")
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces_rect = haar_cascade.detectMultiScale(gray, 1.1, 4)
    for (x,y,w,h) in faces_rect:
        faces_roi = gray[y:y+h,x:x+w]
        label, confidence = face_recognizer.predict(faces_roi)
        cv.putText(img, str(people[label]), (20,20), cv.FONT_HERSHEY_COMPLEX, 1.0, (0,0,0), thickness=2)
        cv.rectangle(img, (x,y), (x+w,y+h), (0,0,0), thickness=5)
    cv.imwrite('static/uploads/check_upload/analyzed.jpg',img)
    os.remove("face_trained.yml")
    return confidence,people[label]

