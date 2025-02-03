## Hi guys, this is a small project where I create some kinds of flame filter for hand gestures
## All the source video is downloaded from Youtube
## Pay attention to the directory path of source code cuz if theyr wrong, code is not gonna work

import cv2 as cv
import mediapipe as mp
import time
import os
import numpy as np




cap = cv.VideoCapture(0)
wCap, hCap = 640,480
cap.set(3, wCap)
cap.set(4, hCap)

def video_processing (img , fire_resized, x1, x2, y1, y2):
    if x1>=0 and y1>=0 and x2<img.shape[1] and y2<img.shape[0]:
        # Convert fire frame to HSV color space for easier color detection
        hsv = cv.cvtColor(fire_resized, cv.COLOR_BGR2HSV)

        # Create a mask to detect the green screen
        mask = cv.inRange(hsv, lower_green, upper_green)

        # Invert the mask to keep the fire only
        mask_inv = cv.bitwise_not(mask)

        # Black-out the area in the fire where the green screen is
        fire_fg = cv.bitwise_and(fire_resized, fire_resized, mask=mask_inv)

        # Extract the region of interest from the frame where the fire will be placed
        roi = img[y1:y2, x1:x2]

        # Black-out the area of the ROI where the fire will be placed
        roi_bg = cv.bitwise_and(roi, roi, mask=mask)

        # Add the fire_fg to the ROI
        combined = cv.add(roi_bg, fire_fg)

        # Place the combined result back into the original frame
        img[y1:y2, x1:x2] = combined

    return img

def video_processing_2 (img , fire_resized):
    x_offset = img.shape[1] // 2 - fire_resized.shape[1] // 2  # Center horizontally
    y_offset = img.shape[0] - fire_resized.shape[0] - 20  # Position at the bottom
    y1, y2 = y_offset, y_offset + fire_resized.shape[0]
    x1, x2 = x_offset, x_offset + fire_resized.shape[1]

    if x1>=0 and y1>=0:
    
        # Convert fire frame to HSV color space for easier color detection
        hsv = cv.cvtColor(fire_resized, cv.COLOR_BGR2HSV)

        # Create a mask to detect the green screen
        mask = cv.inRange(hsv, lower_green, upper_green)

        # Invert the mask to keep the fire only
        mask_inv = cv.bitwise_not(mask)

        # Black-out the area in the fire where the green screen is
        fire_fg = cv.bitwise_and(fire_resized, fire_resized, mask=mask_inv)

        # Extract the region of interest from the frame where the fire will be placed
        roi = img[y1:y2, x1:x2]

        # Black-out the area of the ROI where the fire will be placed
        roi_bg = cv.bitwise_and(roi, roi, mask=mask)

        # Add the fire_fg to the ROI
        combined = cv.add(roi_bg, fire_fg)

        # Place the combined result back into the original frame
        img[y1:y2, x1:x2] = combined
    return img

            





fire_video_1 = cv.VideoCapture("C:/Users/Lenovo/OneDrive/Documents/Python_code/effects/righthand.mp4")
fire_video_2 = cv.VideoCapture("C:/Users/Lenovo/OneDrive/Documents/Python_code/effects/second_effect.mp4")
fire_video = cv.VideoCapture("C:/Users/Lenovo/OneDrive/Documents/Python_code/effects/lefthand.mp4")

lower_green = np.array([35, 40, 40])
upper_green = np.array([85, 255, 255])
# effects = os.listdir(folderPath)
# overlayList = []
# for imPath in effects:
#     image = cv.imread(f'{folderPath}/{imPath}')
#     # print(f'{folderPath}/{imPath}')
#     overlayList.append(image)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    myList = list([])
    success, img = cap.read()
    img = cv.flip(img, 1)
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    # Read the next frame from the fire video
    ret, fire_frame = fire_video.read()
    ret1, fire_frame_1 = fire_video_1.read()
    ret2, fire_frame_2 = fire_video_2.read()
    if not ret:
        fire_video.set(cv.CAP_PROP_POS_FRAMES, 0)
        ret, fire_frame = fire_video.read()
    if not ret1:
        fire_video_1.set(cv.CAP_PROP_POS_FRAMES, 0)
        ret1, fire_frame_1 = fire_video_1.read()
    if not ret2:
        fire_video_2.set(cv.CAP_PROP_POS_FRAMES, 0)
        ret2, fire_frame_2 = fire_video_2.read()

    # Resize fire_frame to a smaller size (e.g., the size of a finger)
    fire_resized = cv.resize(fire_frame, (370, 370))  # Adjust size as needed
    fire_resized_1 = cv.resize(fire_frame_1, (300, 300))
    fire_resized_2 = cv.resize(fire_frame_2, (300, 300))
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id,lm in enumerate(handLms.landmark):
                h,w,c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                myList.append([id,cx,cy])
                cv.circle(img, (cx,cy), 5, (255,0,255), cv.FILLED)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    if len(myList) !=0:
        if myList[8][2]<myList[6][2] and myList[12][2]<myList[10][2] and myList[16][2] < myList[14][2]:
            print("open")
            img = video_processing_2(img, fire_resized)

        elif myList[8][2]<myList[6][2] and myList[12][2]<myList[10][2]:
            x_offset = myList[8][1] - fire_resized_2.shape[1] // 2 - 20
            y_offset = myList[8][2] - fire_resized_2.shape[0] // 2 - 90  # Move fire 10 pixels above the fingertip
            y1, y2 = y_offset, y_offset + fire_resized_2.shape[0]
            x1, x2 = x_offset, x_offset + fire_resized_2.shape[1]
            img = video_processing(img, fire_resized_2,x1,x2,y1,y2)
        elif myList[8][2]<myList[6][2]:
            x_offset = myList[8][1] - fire_resized_1.shape[1] // 2 + 10
            y_offset = myList[8][2] - fire_resized_1.shape[0] // 2 - 70  # Move fire 10 pixels above the fingertip
            y1, y2 = y_offset, y_offset + fire_resized_1.shape[0]
            x1, x2 = x_offset, x_offset + fire_resized_1.shape[1]

            img = video_processing(img, fire_resized_1,x1,x2,y1,y2)


            # # Ensure the ROI is within the frame bounds
            # if x1 >= 0 and y1 >= 0 and x2 < w and y2 < h:
            #     # Convert fire frame to HSV color space for easier color detection
            #     hsv = cv.cvtColor(fire_resized, cv.COLOR_BGR2HSV)

            #     # Create a mask to detect the green screen
            #     mask = cv.inRange(hsv, lower_green, upper_green)

            #     # Invert the mask to keep the fire only
            #     mask_inv = cv.bitwise_not(mask)

            #     # Black-out the area in the fire where the green screen is
            #     fire_fg = cv.bitwise_and(fire_resized, fire_resized, mask=mask_inv)

            #     # Extract the region of interest from the frame where the fire will be placed
            #     roi = img[y1:y2, x1:x2]

            #     # Black-out the area of the ROI where the fire will be placed
            #     roi_bg = cv.bitwise_and(roi, roi, mask=mask)

            #     # Add the fire_fg to the ROI
            #     combined = cv.add(roi_bg, fire_fg)

            #     # Place the combined result back into the original frame
            #     img[y1:y2, x1:x2] = combined



    
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv.putText(img,str(int(fps)), (10,70), cv.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv.imshow("IMG",img)
    cv.waitKey(1)

