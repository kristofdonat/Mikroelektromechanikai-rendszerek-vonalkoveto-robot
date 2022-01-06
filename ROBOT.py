import tweepy
import random
from gpiozero import Robot, LineSensor
from time import sleep

def tweet(uzenet):
    auth = tweepy.OAuthHandler('Felhaszn_kulcs','Felhaszn_jelszo')
    auth.set_access_token('API_token','API_kulcs')
    api = tweepy.API(auth)
    randomszam = random.randrange(1,100)
    api.update_status(str(uzenet))
    print("sikeresen tweetelve az, hogy ", uzenet)

def configure_robot():
    robot = Robot(left=(5, 6), right=(23, 24))
    left_sensor = LineSensor(17)
    right_sensor = LineSensor(27)

def start(seconds):
    robot.source = motor_speed()
    sleep(seconds)

def stop():
    robot.stop()
    robot.source = None
    robot.close()
    left_sensor.close()
    right_sensor.close()

def motor_speed():
    while True:
        left_detect  = int(left_sensor.value)
        right_detect = int(right_sensor.value)
        ## Stage 1
        if left_detect == 0 and right_detect == 0:
            left_mot = 1
            right_mot = 1
        ## Stage 2
        if left_detect == 0 and right_detect == 1:
            left_mot = -1
        if left_detect == 1 and right_detect == 0:
            right_mot = -1
        #print(r, l)
        yield (right_mot * speed, left_mot * speed)


