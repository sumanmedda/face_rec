# NOTE : Images sizes are set to : 216 x 216
# importing the cv2 package for video capture
from datetime import datetime
import os
import pickle
import cv2
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
# initializong rtdb url for connection 
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://facerec-cec69-default-rtdb.firebaseio.com/",
    'storageBucket':"facerec-cec69.appspot.com"
})

bucket = storage.bucket()
imgStudent = []
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

# creating mode types
modeType = 0 
counter = 0 
id = -1

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
    imgBackground[44:44+633,808:808+414] = imgModeList[modeType]
    
    if faceCurrFrame:
        for encodeFace, faceLoc in zip(encodeCurrFrame,faceCurrFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
            matchIndex = np.argmin(faceDis)
            
            if matches[matchIndex]:
                y1,x2,y2,x1 = faceLoc
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                bbox = 55+x1,162+y1,x2-x1,y2-y1
                imgBackground = cvzone.cornerRect(imgBackground,bbox,rt=0)
                id = studentIds[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgBackground,"Loading...",(275,400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1
        
        if counter != 0:
            # if counter is 1 then downloading the data from db
            if counter == 1:
                # getting student info
                studentInfo = db.reference(f'students/{id}').get()
                # getting images of students from storage and joining with image extension saved in firebase storage
                blob = bucket.get_blob(f'images/{id}.jpg')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)
                # update Data of attendance time
                dateTimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S"),
                secondsElapsed = (datetime.now()-dateTimeObject).total_seconds()
                # need to add one day logic that after 1 day only student can mark present
                if secondsElapsed > 30:    
                    # update Data of attendance
                    ref = db.reference(f'students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[44:44+633,808:808+414] = imgModeList[modeType]
                    
                    
            if modeType != 3:
                if 10<counter<20:
                    modeType = 2
                
                imgBackground[44:44+633,808:808+414] = imgModeList[modeType]
                    
                if counter <= 10:
                    # adjusting and showing the downloaded data on the screen
                    cv2.putText(imgBackground, str(studentInfo['total_attendance']),(861,125),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                    cv2.putText(imgBackground, str(studentInfo['major']),(1006,550),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                    cv2.putText(imgBackground, str(studentInfo['id']),(1006,493),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                    cv2.putText(imgBackground, str(studentInfo['standings']),(910,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                    cv2.putText(imgBackground, str(studentInfo['year']),(1025,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                    cv2.putText(imgBackground, str(studentInfo['starting_year']),(1125,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                    # centering text of name as it could be of any length
                    (w,h), _ = cv2.getTextSize(studentInfo['name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
                    offset = (414-w)//2 
                    cv2.putText(imgBackground, str(studentInfo['name']),(808+offset,445),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,50),1)
                    
                    imgBackground[175:175+216,909:909+216] = imgStudent
            
                counter += 1
                
                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44+633,808:808+414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0        
            
    
    cv2.imshow("webcam", img)
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)