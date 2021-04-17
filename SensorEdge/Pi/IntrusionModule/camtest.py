from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.rotation = 90

try:
    camera.start_preview()
    sleep(5)
    camera.stop_preview()
except KeyboardInterrupt:
    camera.stop_preview()