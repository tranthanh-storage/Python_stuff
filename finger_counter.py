## This is finger counter code using OpenCV and a class, which is built in file "lesson1"

import cv2 as cv
import time
import os
import lesson1 as htm

wCam, hCam = 640,480
cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "C:/Users/Lenovo/OneDrive/Documents/Python_code/recognition"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv.imread(f'{folderPath}/{imPath}')
    # print(f'{folderPath}/{imPath}')
    overlayList.append(image)
pTime = 0

detector = htm.handDetector()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findLocations(img)
    # print(lmList)

    if len(lmList) !=0:
        if lmList[8][2] <lmList[6][2] and lmList[12][2]<lmList[10][2] and lmList[16][2]<lmList[14][2] and lmList[20][2]<lmList[19][2] and lmList[4][2]<lmList[2][2]:
            print("5")
        elif  lmList[8][2] <lmList[6][2] and lmList[12][2]<lmList[10][2] and lmList[16][2]<lmList[14][2] and lmList[20][2]<lmList[19][2]:
            print("4")
        elif lmList[8][2] <lmList[6][2] and lmList[12][2]<lmList[10][2] and lmList[16][2]<lmList[14][2]:
            print("3")
        elif lmList[8][2] <lmList[6][2] and lmList[12][2]<lmList[10][2]:
            print("2")
        elif lmList[8][2] <lmList[6][2]:
            print("1")
        else:
            print("closed")


    img[0:220,0:200] = overlayList[6]

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv.putText(img,f'{int(fps)}',(400,70), cv.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)

    cv.imshow("IMG",img)
    cv.waitKey(1)