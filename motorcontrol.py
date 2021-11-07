from gpiozero import Robot
import time
'''
from gpiozero import Motor
motor1 = Motor(19,16)
motor2 = Motor(20,26)
motor2.forward()
motor1.forward()
time.sleep(100)
motor2.stop()
motor1.stop()
time.sleep(1)
motor2.backward()
motor1.backward()
time.sleep(10)
'''
robot = Robot(right=(19,16),left=(26,20))
count = 0


robot.forward()
time.sleep(0.8)
robot.stop()
robot.right()
time.sleep(0.5)
robot.stop()

'''
while True:
    robot.forward()
    time.sleep(0.5)
    robot.left()
    time.sleep(0.5)
    robot.stop()
    time.sleep(3)
    robot.right()
    time.sleep(0.37)
    robot.stop()
    time.sleep(3)
    count += 1
    if count >= 1:
        break
'''