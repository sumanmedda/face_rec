# importing the cv2 package for video capture
import os
import cv2

#using the webcam
cap = cv2.VideoCapture(0)

# croping the webcam to specific size so it fits into the backgroundimg
cap.set(3,640)
cap.set(4,480)

# getting the images
imgBackground = cv2.imread('Resources/background.png')
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
#  using for loop getting all images
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))

# function to run webcam and fitting the images on space
while True:
    success, img = cap.read()
    imgBackground[162:162+480,55:55+640] = img
    imgBackground[44:44+633,808:808+414] = imgModeList[1]
    
    cv2.imshow("webcam", img)
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)