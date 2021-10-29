import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BCM)  
# GPIO 23 set up as input. It is pulled up to stop false signals  
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)   
# now the program will do nothing until the signal on port 23   
# starts to fall towards zero. This is why we used the pullup  
# to keep the signal high and prevent a false interrupt  
try:  
    GPIO.wait_for_edge(23, GPIO.FALLING)   
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()