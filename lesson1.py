import mediapipe as mp
import cv2 as cv
import time

# cap = cv.VideoCapture(0)

# mpHands = mp.solutions.hands
# hands = mpHands.Hands()
# mpDraw = mp.solutions.drawing_utils

# pTime = 0
# cTime = 0


# while True:
#     success,img = cap.read()
#     imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
#     results = hands.process(imgRGB)
#     if  results.multi_hand_landmarks:
#         for handLms in results.multi_hand_landmarks:
#             for id, lm in enumerate(handLms.landmark):
#                 h,w,c = img.shape
#                 cx, cy = int(lm.x*w), int(lm.y*h)
#                 print(id,cx,cy)
#                 if id == 0:
#                     cv.circle(img, (cx,cy), 25, (255,0,255), cv.FILLED)
#             mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
#     cTime = time.time()
#     fps = 1/(cTime-pTime)
#     pTime = cTime

#     cv.putText(img,str(int(fps)), (10,70), cv.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    
#     cv.imshow("IMG",img)
#     cv.waitKey(1)


class handDetector():
    def __init__(self, mode = False, max_num_hands = 2, model_complexity = 1, min_detection_confidence = 0.5, min_tracking_confidence = 0.5):
        self.mode = mode
        self.maxHands = max_num_hands
        self.modComplex = model_complexity
        self.detecCon = min_detection_confidence
        self.trackCon = min_tracking_confidence
        
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modComplex, self.detecCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands (self,img, draw = True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if  self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
                # for id, lm in enumerate(handLms.landmark):
                #     h,w,c = img.shape
                #     cx, cy = int(lm.x*w), int(lm.y*h)
                #     print(id,cx,cy)
                #     if id == 0:
                #         cv.circle(img, (cx,cy), 25, (255,0,255), cv.FILLED)
                
        return img
    def findLocations (self,img, handNo = 0):
        myList = list([])
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h,w,c = img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    myList.append([id,cx,cy])
                    cv.circle(img, (cx,cy), 5, (255,0,255), cv.FILLED)
        return myList








def main ():
    cap = cv.VideoCapture(0)
    pTime = 0
    cTime = 0
    detector = handDetector()
    while True:
        success,img = cap.read()
        img = detector.findHands(img)
        myList = detector.findLocations(img)
        if len(myList)!=0:
            print(myList[2])
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv.putText(img,str(int(fps)), (10,70), cv.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    
        cv.imshow("IMG",img)
        cv.waitKey(1)



if __name__ == "__main__":
    main()