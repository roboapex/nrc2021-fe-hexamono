import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

while(1):
    # Take each frame
    _, frame = cap.read()
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # define range of red color in HSV
    lower_red = np.array([0,50,50])
    upper_red = np.array([15,255,255])
    # Threshold the HSV image to get only red colors
    maskR = cv.inRange(hsv, lower_red, upper_red)
    redcnts = cv.findContours(maskR.copy(),
                              cv.RETR_EXTERNAL,
                              cv.CHAIN_APPROX_SIMPLE)[-2]
    if len(redcnts)>0:
        red_area = max(redcnts, key=cv.contourArea)
        (xr,yr,wr,hr) = cv.boundingRect(red_area)
        cv.rectangle(frame,(xr,yr),(xr+wr, yr+hr),(255,255,255),2)
    # Bitwise-AND mask and original image
    res = cv.bitwise_and(frame,frame, mask= maskR)
    cv.imshow('frame',frame)
    cv.imshow('mask',maskR)
    cv.imshow('res',res)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
cv.destroyAllWindows()