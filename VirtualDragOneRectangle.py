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
cx, cy, w, h = 100, 100, 200, 200 #Defining rectangle center-x, center-y, width and height
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
            cursor = hands[0]['lmList'][8][:2]  #Getting the postion of the x and y coordinates of the finger tip
            if cx-w//2< cursor[0] < cx+w//2 and cy-h//2< cursor[1] < cy+h//2:
                colorR = 255,255,0
                cx, cy = cursor #Dragging the rectangle using finger
        else:
            colorR = 255,0,255
    # cv2.rectangle(img, (cx-w//2,cy-h//2), (cx+w//2,cy+h//2), colorR, cv2.FILLED) #Creating a dynamic solid rectangle on the live camera screen
    cv2.rectangle(img, (cx-w//2,cy-h//2), (cx+w//2,cy+h//2), colorR, 3) #Creating a dynamic solid rectangle on the live camera screen
    cvzone.cornerRect(img, (cx-w//2,cy-h//2, w,h), 20, rt=0) #Drawing the corners of all of the rectangles
    
    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break