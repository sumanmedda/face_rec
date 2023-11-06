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
