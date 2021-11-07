from gpiozero import DistanceSensor
import time
sensor1 = DistanceSensor(echo=6,trigger=12,max_distance=2.0,threshold_distance=0.3)
sensor2 = DistanceSensor(echo=17,trigger=18,max_distance=2.0,threshold_distance=0.3)
while True:
    distance = sensor1.distance * 100
    print("Distance1 : %.1f" % distance)
    distance2 = sensor2.distance * 100
    print("Distance2 : %.1f" % distance2)
    time.sleep(1)