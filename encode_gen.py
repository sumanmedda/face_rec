import os
import cv2
import face_recognition
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
# initializong rtdb url for connection 
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://facerec-cec69-default-rtdb.firebaseio.com/",
    'storageBucket':"gs://facerec-cec69.appspot.com"
})


# getting the images for attendance
folderPath = 'images'
pathList = os.listdir(folderPath)
imgList = []
studentIds = []
#  using for loop getting all images and ids of students
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    studentIds.append(os.path.splitext(path)[0])
 
def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        if img is not None:
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
    
    return encodeList

# Encoding
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown,studentIds]

file = open("EncodeFile.p","wb")
pickle.dump(encodeListKnownWithIds,file)
file.close()
#  saving the list of encoding list with student ids

