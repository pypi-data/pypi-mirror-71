# RPI-Servo
Control servos with python !

Example to run a servo connected to pin 3 and angle 90:

import RPI.GPIO as GPIO
import piServo
servo = piServo.Servo(3)
servo.initServo()
servo.setAngle(90)
servo.stopServo()
GPIO.cleanup()
