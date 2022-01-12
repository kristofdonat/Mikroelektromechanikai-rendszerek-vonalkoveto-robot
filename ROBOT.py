import tweepy
import random
from gpiozero import Robot, LineSensor
from time import sleep
from PIL import Image, ImageOps

auth = tweepy.OAuthHandler('xWaOHMW9GSNgjsr8ShNu3LO1R','0TgRFHwvwouqziWclqtISPWajliqoR0RjAwyNJmyfQUtjXd5gg')
auth.set_access_token('1450813593969123330-r1sSJVNPCUujRXbdNa6kbrQR9Iz3qJ','POBpiQTXpVU2UWKXOPuRHsi8dpUgWQKaHgOnktBGAdNsM')
api = tweepy.API(auth)

def tweet(uzenet):
    api.update_status(str(uzenet))
    print("sikeresen tweetelve az, hogy ", uzenet)

robot = Robot(right=(5, 6), left=(24, 23))
left_sensor = LineSensor(27)
right_sensor= LineSensor(17)

speed = -1

bal = []
jobb = []

def motor_speed():
    while True:
        left_detect  = int(left_sensor.value)
        right_detect = int(right_sensor.value)
        bal.append(left_detect)
        jobb.append(right_detect)
        ## Stage 1
        if left_detect == 0 and right_detect == 0:
            left_mot = -0.7
            right_mot = -0.7
        if left_detect == 1 and right_detect == 1:
            left_mot = -0.7
            right_mot = -0.7
        ## Stage 2
        if left_detect == 0 and right_detect == 1:
            left_mot = 0
            right_mot = -0.7
        if left_detect == 1 and right_detect == 0:
            right_mot = 0
            left_mot = -0.7
        #print(r, l)
        yield (right_mot * speed, left_mot * speed)
        
def stop():
    robot.stop()
    robot.source = None
    robot.close()
    left_sensor.close()
    right_sensor.close()

def go(seconds):
    robot.source = motor_speed()
    sleep(seconds)
    stop()
        



#tweet("Elindultam végre!!!")
go(5)


def kiir(tabla):
    for i in range(len(tabla)):
        if "X" in tabla[i]:
            for j in range(len(tabla[i])):
                if tabla[i][j] == []:
                    print("O", end = "")
                if tabla[i][j] == 'X':
                    print("X", end = "")
            print("")
    print("Tábla kiírva!")

ut = ["S"]
x_helye = [0, 0]
def bovites(merre):
    global ut
    if merre == "jobb":
        for i in range(len(ut)):
            ideigl = []
            for j in range(len(ut[i])):
                ideigl.append(ut[i][j])
            ideigl.append([])
            ut[i] = ideigl
    if merre == "le":
        if len(ut[0]) == 1:
            ut.append([[]])
        else:
            ut.append([])
        if len(ut[0]) != 1:
            for i in range(len(ut[0])):
                ut[-1].append([])
    if merre == "bal":
        x_helye[1] += 1
        for i in range(len(ut)):
            ideigl = []
            ideigl.append([])
            for j in range(len(ut[i])):
                ideigl.append(ut[i][j])
            ut[i] = ideigl
    if merre == "fel":
        x_helye[0] += 1
        ideigl = [[]]
        for i in range(len(ut[0])):
            ideigl[0].append([])
        for i in range(len(ut)):
            ideigl.append(ut[i])
        ut = ideigl

def draw(hova):
    if hova == "fel":
        bovites(hova)
        ut[x_helye[0]-1][x_helye[1]] = "X"
        x_helye[0] -=1
    if hova == "le":
        bovites(hova)
        ut[x_helye[0]+1][x_helye[1]] = "X"
        x_helye[0] +=1
    if hova == "bal":
        bovites(hova)
        ut[x_helye[0]][x_helye[1]-1] = "X"
        x_helye[1] -=1
    if hova == "jobb":
        bovites(hova)
        ut[x_helye[0]][x_helye[1]+1] = "X"
        x_helye[1] +=1

#MOZGATÁS/BEOLVASÁS
orientations = [[0, 3, 1], [1, 0, 2], [2, 1, 3], [3, 2, 0]]   # 0 = észak, 1 kelet, 2 dél, 3 nyugat
#szerkezet [orientation, previous(lista index szerint), nex(lista index szerint)]

def reorient(orientation, turn):
    if turn == -1:
        return orientations[orientations[orientation][1]][0]
    if turn == 1:
        return orientations[orientations[orientation][2]][0]
        
    
orientation = 0
def move(hova, orientation):
    if orientation == 0: # Észak
        if hova == "előre":
            draw("fel")
        if hova == "balra":
            draw("fel")
            draw("bal")
        if hova == "jobbra":
            draw("fel")
            draw("jobb")
    if orientation == 1: # Kelet
        if hova == "előre":
            draw("jobb")
        if hova == "balra":
            draw("jobb")
            draw("fel")
        if hova == "jobbra":
            draw("jobb")
            draw("le")
    if orientation == 2: # Dél
        if hova == "előre":
            draw("le")
        if hova == "balra":
            draw("le")
            draw("jobb")
        if hova == "jobbra":
            draw("le")
            draw("bal")
    if orientation == 3: # Nyugat
        if hova == "előre":
            draw("bal")
        if hova == "balra":
            draw("bal")
            draw("le")
            draw(hova)
        if hova == "jobbra":
            draw("bal")
            draw("fel")

bovites("jobb")
bovites("bal")
bovites("le")
bovites("fel")

#ideiglenes beolvasásból "rajzolás"
balcount = 0
jobbcount = 0
countsensitivitation = 50
for i in range(len(jobb)):
    if jobb[i] == 1 and bal[i] == 1:
        balcount = 0
        jobbcount = 0
        move("előre", orientation)
        move("előre", orientation)
        
    if jobb[i] == 0 and bal[i] == 0:
        balcount = 0
        jobbcount = 0
        #move("le", balcount, jobbcount)
        
    if jobb[i] == 0 and bal[i] == 1:
        jobbcount += 1
        balcount = 0
        move("jobbra", orientation)
        
    if jobb[i] == 1 and bal[i] == 0:
        balcount+=1
        jobbcount = 0
        move("balra", orientation)
    if balcount >= countsensitivitation:
        orientation = reorient(orientation, -1)
        balcount = 0
    if jobbcount >= countsensitivitation:
        orientation = reorient(orientation, 1)
        jobbcount = 0


#kiir(ut)
width = len(ut[0])
height = len(ut)
img = Image.new('RGB', [height,width], 255)
data = img.load()

ut2 = []
for i in range(len(ut)):
    ut2.append([])
    for j in range(len(ut[i])):
        if ut[i][j] == []:
            ut2[i].append(False)
            data[i,j] = (255, 255, 255)
        if ut[i][j] == 'X':
            ut2[i].append(True)
            data[i,j] = (0, 0, 0)

img = ImageOps.flip(img)
img = img.rotate(-90)
img.save('map.png')


print("lefutott")
img.show()

img = "/home/pi/Documents/Python/map.png"
media = api.media_upload(img)
tweet = "Ma is mentem egy jót"
post_result = api.update_status(status=tweet, media_ids=[media.media_id])

#/home/pi/Documents/Python



