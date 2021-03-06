import time
import cv2 as cv
import numpy as np
cap = cv.VideoCapture(0)
from gpiozero import Robot
from gpiozero import DistanceSensor
import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BCM)  
# GPIO 23 set up as input. It is pulled up to stop false signals  
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)   
# now the program will do nothing until the signal on port 23   
# starts to fall towards zero. This is why we used the pullup  
# to keep the signal high and prevent a false interrupt  
'''
try:  
    GPIO.wait_for_edge(23, GPIO.FALLING)   
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
'''
GPIO.cleanup()
turn = 0.6
count = 0
rest = 0.1
forward = 1/80
robot = Robot(right=(19,16),left=(26,20))
sensor1 = DistanceSensor(echo=6,trigger=12,max_distance=2.0,threshold_distance=0.3)
sensor2 = DistanceSensor(echo=17,trigger=18,max_distance=2.0,threshold_distance=0.3)

robot.forward()
time.sleep(forward*64)
robot.stop()
time.sleep(rest)
robot.right()
time.sleep(turn)
robot.stop()
time.sleep(rest)

while True:
    distance1 = sensor1.distance * 100
    distance2 = sensor2.distance * 100
    print(distance1)
    print(distance2)
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
    
    cv.imshow('frame',frame)

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
    cv.imshow('frame',frame)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
    if ((xr > 0) or (yr > 0) or (wr > 0) or (hr > 0)):
        robot.right()
        time.sleep(turn)
        robot.forward()
        time.sleep(forward*25)
        robot.left()
        time.sleep(turn)
        robot.forward()
        time.sleep(forward*25)
        robot.left()
        time.sleep(turn)
        robot.forward()
        time.sleep(forward*25)
        robot.right()
        time.sleep(turn)
        robot.stop()
        print("red")
        #move
    elif ((xg > 0) or (yg > 0) or (wg > 0) or (hg > 0)):
        robot.left()
        time.sleep(turn)
        robot.forward()
        time.sleep(forward*25)
        robot.right()
        time.sleep(turn)
        robot.forward()
        time.sleep(forward*25)
        robot.right()
        time.sleep(turn)
        robot.forward()
        time.sleep(forward*25)
        robot.left()
        time.sleep(turn)
        robot.stop()
        print("green")
        #move
    if ((distance1 == distance2) or (distance2 < distance1) or ((distance2 >= 20) and (distance2 <= 40))):
        robot.right()#turn right first
        time.sleep(1)
        #update cam
        _, frame = cap.read()
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        maskR = cv.inRange(hsv, lower_red, upper_red)
        redcnts = cv.findContours(maskR.copy(),
                              cv.RETR_EXTERNAL,
                              cv.CHAIN_APPROX_SIMPLE)[-2]
        maskG = cv.inRange(hsv, lower_green, upper_green)
        greencnts = cv.findContours(maskG.copy(),
                                cv.RETR_EXTERNAL,
                                cv.CHAIN_APPROX_SIMPLE)[-2]
        if len(redcnts)>0:
            red_area = max(redcnts, key=cv.contourArea)
            (xr,yr,wr,hr) = cv.boundingRect(red_area)
            cv.rectangle(frame,(xr,yr),(xr+wr, yr+hr),(255,255,255),2)
        maskG = cv.inRange(hsv, lower_green, upper_green)
        greencnts = cv.findContours(maskG.copy(),
                              cv.RETR_EXTERNAL,
                              cv.CHAIN_APPROX_SIMPLE)[-2]
        if len(greencnts)>0:
            green_area = max(greencnts, key=cv.contourArea)
            (xg,yg,wg,hg) = cv.boundingRect(green_area)
            cv.rectangle(frame,(xg,yg),(xg+wg, yg+hg),(255,255,255),2)
        if ((xr > 0) or (yr > 0) or (wr > 0) or (hr > 0)): #check for presence of red
            #move
            robot.right()
            time.sleep(turn)
            robot.forward()
            time.sleep(forward*25)
            robot.left()
            time.sleep(turn)
            robot.forward()
            time.sleep(forward*25)
            robot.left()
            time.sleep(turn)
            robot.forward()
            time.sleep(forward*25)
            robot.right()
            time.sleep(turn)
            robot.stop()
            print("red")
        elif ((xg > 0) or (yg > 0) or (wg > 0) or (hg > 0)): #checks presence of green
            #move
            robot.left()
            time.sleep(turn)
            robot.forward()
            time.sleep(forward*25)
            robot.right()
            time.sleep(turn)
            robot.forward()
            time.sleep(forward*25)
            robot.right()
            time.sleep(turn)
            robot.forward()
            time.sleep(forward*25)
            robot.left()
            time.sleep(turn)
            robot.stop()
            print("green")
    else:
        print("ok")
        robot.forward()
        time.sleep(forward*25)
        robot.stop()
        '''
        N = 0
        while N <= 3:
            distance1 = sensor1.distance * 100
            if distance1 > 10:
                robot.right()
                time.sleep(0.1)
            distance1 = sensor1.distance * 100
            if distance1 < 10:
                robot.left()
                time.sleep(0.1)
            distance1 = sensor1.distance * 100
            if distance1 == 10:
                robot.forward()
                time.sleep(1)
            distance1 = sensor1.distance * 100
            N += 1
        
        while distance1 != 10:
            distance1 = sensor1.distance * 100
            if distance1 > 10:
                robot.right()
                time.sleep(0.1)
            distance1 = sensor1.distance * 100
            if distance1 < 10:
                robot.left()
                time.sleep(0.1)
            distance1 = sensor1.distance * 10
            '''
        #move certain dist
    #update cam
    _, frame = cap.read()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    maskR = cv.inRange(hsv, lower_red, upper_red)
    redcnts = cv.findContours(maskR.copy(),
                            cv.RETR_EXTERNAL,
                            cv.CHAIN_APPROX_SIMPLE)[-2]
    maskG = cv.inRange(hsv, lower_green, upper_green)
    greencnts = cv.findContours(maskG.copy(),
                            cv.RETR_EXTERNAL,
                            cv.CHAIN_APPROX_SIMPLE)[-2]
    if len(redcnts)>0:
        red_area = max(redcnts, key=cv.contourArea)
        (xr,yr,wr,hr) = cv.boundingRect(red_area)
        cv.rectangle(frame,(xr,yr),(xr+wr, yr+hr),(255,255,255),2)
    maskG = cv.inRange(hsv, lower_green, upper_green)
    greencnts = cv.findContours(maskG.copy(),
                            cv.RETR_EXTERNAL,
                            cv.CHAIN_APPROX_SIMPLE)[-2]
    if len(greencnts)>0:
        green_area = max(greencnts, key=cv.contourArea)
        (xg,yg,wg,hg) = cv.boundingRect(green_area)
        cv.rectangle(frame,(xg,yg),(xg+wg, yg+hg),(255,255,255),2)
        #move
    count += 1
    if count == 18:
        break
cv.destroyAllWindows()