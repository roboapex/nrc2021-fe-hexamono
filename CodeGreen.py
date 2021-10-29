import cv2 as cv
import numpy as np
cap = cv.VideoCapture(0)
while(1):
    # Take each frame
    _, frame = cap.read()
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # define range of green color in HSV
    lower_green = np.array([35,50,50])
    upper_green = np.array([75,255,255])
    # Threshold the HSV image to get only green colors
    maskG = cv.inRange(hsv, lower_green, upper_green)
    greencnts = cv.findContours(maskG.copy(),
                              cv.RETR_EXTERNAL,
                              cv.CHAIN_APPROX_SIMPLE)[-2]
    if len(greencnts)>0:
        green_area = max(greencnts, key=cv.contourArea)
        (xg,yg,wg,hg) = cv.boundingRect(green_area)
        cv.rectangle(frame,(xg,yg),(xg+wg, yg+hg),(255,255,255),2)
    # Bitwise-AND mask and original image
    res = cv.bitwise_and(frame,frame, mask= maskG)
    cv.imshow('frame',frame)
    cv.imshow('mask',maskG)
    cv.imshow('res',res)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
cv.destroyAllWindows()