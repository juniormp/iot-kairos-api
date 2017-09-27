import requests
import json
import base64
import RPi.GPIO as GPIO
import datetime
from picamera import PiCamera
from time import sleep
from gpiozero import MotionSensor

pir = MotionSensor(4)
camera = PiCamera()
camera.resolution = (250, 250)

def take_picture():
    camera.start_preview()
    sleep(1)
    name = '/home/pi/Desktop/%s.jpg' % datetime.datetime.now()
    camera.capture(name)
    camera.stop_preview()
    return name

def encode_image(image_path):
    image = open(image_path, 'rb')
    image_read = image.read()
    image_64_encode = base64.encodestring(image_read) 
    return image_64_encode

def send_image(image):
    url = 'https://face-recognition.mybluemix.net/imagens'
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data = {"imagem": image}
    requests.post(url, data = json.dumps(data), headers = headers)

while True:
    pir.wait_for_motion()
    path_image = take_picture()
    encoded = encode_image(path_image)
    send_image(encoded)
    pir.wait_for_no_motion()
