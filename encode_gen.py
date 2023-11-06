import os
import cv2
import face_recognition
import pickle

# getting the images for attendance
folderPath = 'Images'
pathList = os.listdir(folderPath)
imgList = []
studentIds = []
#  using for loop getting all images and ids of students
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    studentIds.append(os.path.splitext(path)[0])

def findEncodings(imagesList):
    encodeList = [ ]
    for img in imagesList:
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

