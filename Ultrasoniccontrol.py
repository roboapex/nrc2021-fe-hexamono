from gpiozero import DistanceSensor
import time
sensor1 = DistanceSensor(echo=23,trigger=24,max_distance=2.0,threshold_distance=0.3)
sensor2 = DistanceSensor(echo=27,trigger=22,max_distance=2.0,threshold_distance=0.3)
while True:
    distance = sensor1.distance * 100
    print("Distance1 : %.1f" % distance)
    distance2 = sensor2.distance * 100
    print("Distance2 : %.1f" % distance2)
    time.sleep(1)