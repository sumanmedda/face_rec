# importing the cv2 package for video capture
import os
import pickle
import cv2
import face_recognition
import numpy as np
import cvzone

#using the webcam
cap = cv2.VideoCapture(0)

# croping the webcam to specific size so it fits into the backgroundimg
cap.set(3,640)
cap.set(4,480)

# getting the images
imgBackground = cv2.imread('resources/background.png')
folderModePath = 'resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
#  using for loop getting all images
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))

# load encoded file
file = open("EncodeFile.p",'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown,studentIds = encodeListKnownWithIds
print(studentIds)

# function to run webcam and fitting the images on space
while True:
    success, img = cap.read()
    # compressing images
    imgs = cv2.resize(img, (0,0), None, 0.25, 0.25)
    if imgs is not None:
            imgs = cv2.cvtColor(imgs,cv2.COLOR_BGR2RGB)
    
    faceCurrFrame = face_recognition.face_locations(imgs)
    encodeCurrFrame = face_recognition.face_encodings(imgs, faceCurrFrame)
    
    imgBackground[162:162+480,55:55+640] = img
    imgBackground[44:44+633,808:808+414] = imgModeList[1]
    
    for encodeFace, faceLoc in zip(encodeCurrFrame,faceCurrFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        matchIndex = np.argmin(faceDis)
        
        if matches[matchIndex]:
            y1,x2,y2,x1 = faceLoc
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            bbox = 55+x1,162+y1,x2-x1,y2-y1
            imgBackground = cvzone.cornerRect(imgBackground,bbox,rt=0)
            
    
    cv2.imshow("webcam", img)
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)