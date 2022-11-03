#Importing all Libraries:
import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np

cap = cv2.VideoCapture(0)

#Setting Camera Width:
cap.set(3,1280)
#Setting Camera Height:
cap.set(4,720)
#Setting Hand Detector Confidence:
detector = HandDetector(detectionCon=0.8, maxHands=2)
####
colorR = (255,0,255)
cx, cy, w, h = 100, 100, 100, 100 #Defining rectangle center-x, center-y, width and height


class DragRectangle():
    def __init__(self, CenterPosition, size=[100,100]):
        self.CenterPosition = CenterPosition
        self.size = size

    def update(self,cursor):
        cx,cy = self.CenterPosition
        w,h = self.size
        #If index finger tip is inside the rectangle region
        if cx-w//2< cursor[0] < cx+w//2 and cy-h//2< cursor[1] < cy+h//2:
                
                self.CenterPosition = cursor #Dragging the rectangle using finger

rectangleList = [] #Empty list to store all the rectangles
for x in range(4):
    rectangleList.append(DragRectangle([x*150+75,75]))

#Enabling Camera Settings:
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1) #Flipping camera horizontally
    hands, img = detector.findHands(img) #This code will find the hands and their landmarks using the live camera 
    if hands:
        # l, _, _ = detector.findDistance(hands[0]['lmList'][8][:2], hands[0]['lmList'][12][:2], img) #Finding distance between index finger and middle finger tips and drawing the distance between the two finger tips.
        l, _ = detector.findDistance(hands[0]['lmList'][8][:2], hands[0]['lmList'][12][:2]) #Finding distance between index finger and middle finger tips and not drawing the distance between the two finger tips.
        # print(l)
        #If distance (l) is less than 40, rectangle is clicked and is dragable, else rectangle is not clicked and not dragable.
        if l<35:
            cursor = hands[0]['lmList'][8][:2]  #Getting the landmark postion of the x and y coordinates of the index finger tip
            colorR = 255,255,0
            for rectangle in rectangleList:
                rectangle.update(cursor)

        else:
            colorR = 255,0,255
    #Code to draw the solid rectangles:
    # for rectangle in rectangleList:
    #     cx,cy = rectangle.CenterPosition
    #     w,h = rectangle.size
    #     cv2.rectangle(img, (cx-w//2,cy-h//2), (cx+w//2,cy+h//2), colorR, cv2.FILLED) #Creating a dynamic rectangle on the live camera screen
    #     cvzone.cornerRect(img, (cx-w//2,cy-h//2, w,h), 20, rt=0) #Drawing the corners of all of the rectangles
 
    #Code to draw the rectangles:
    for rectangle in rectangleList:
        cx,cy = rectangle.CenterPosition
        w,h = rectangle.size
        cv2.rectangle(img, (cx-w//2,cy-h//2), (cx+w//2,cy+h//2), colorR, 3) #Creating a dynamic rectangle on the live camera screen
        cvzone.cornerRect(img, (cx-w//2,cy-h//2, w,h), 20, rt=0) #Drawing the corners of all of the rectangles
    

    ## Draw Solid Transparent Rectangles
    # imgNew = np.zeros_like(img, np.uint8)
    # for rectangle in rectangleList:
    #     cx, cy = rectangle.CenterPosition
    #     w, h = rectangle.size
    #     cv2.rectangle(imgNew, (cx - w // 2, cy - h // 2),
    #                   (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)
    #     cvzone.cornerRect(imgNew, (cx - w // 2, cy - h // 2, w, h), 20, rt=0) #Drawing the corners of all of the rectangles
 
    # out = img.copy()
    # alpha = 0.5
    # mask = imgNew.astype(bool)
    # out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask] 

    ##############
    # cv2.imshow('Image', out) #For showing solid transparent rectangle boxes
    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break