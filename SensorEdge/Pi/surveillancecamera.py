import time
from datetime import datetime
from picamera import PiCamera
from queue import Queue
import sqlite3
import serial

filePath = '/home/pi/Documents/projectgg/files'

stop = False

# DB_NAME
DB_NAME = 'shs'

#Connection to DB
conn = sqlite3.connect(DB_NAME)

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30

def handleMessage(smsg):
    params = smsg.split()
    if params[1] == "int":
        print("taking video")
        fileName =  datetime.now().strftime("%Y%m%d%H%M%S") + '.h264'
        camera.start_recording(filePath + "/" + fileName)
        time.sleep(5)
        camera.stop_recording()
        curr = conn.cursor()
        curr.execute("INSERT INTO intrusions (edgeconnector, videofile) VALUES (?,?)", (int(params[0]), fileName))
        conn.commit()
        curr.close()
        print("Intrusion Detected, Video File:", fileName)

def socketListener():
    host = socket.gethostname()
    port = 6789
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    
    while not stop:
        s.listen(1)
        client_socket, address = s.accept()
        # s.setblocking(False)
        message = ""
        
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            message += data
            if not data:
                break
        print("Message received:", message)
        queue.add(message)
        client_socket.close()

def serialListener():
    state = 0
    while not stop:
        while not queue.empty():
            param = queue.get()
            if param == "arm":
                state = 0
                ser.writeLine(str.encode("arm$0/r/n"))
            elif param == "unarm":
                state = 1
                ser.writeLine(str.encode("unarm$1/r/n"))
        if state == 0:
            lines = ser.readlines()
            if lines:
                for line in lines:
                   smsg = line.decode("utf-8").strip()
                   if len(smsg) > 0:
                       handleMessage(smsg) 

try:
    print("Edge Connector Online")
    print("Listening on /dev/ttyACM0... Press CTRL+C to exit")
    print("Also listening on port 6789 for web services")
    queue = Queue()
    ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1)
    serialListener()
except KeyboardInterrupt:
    stop = True
    if ser.is_open:
        ser.close()
    # conn.close()
    print("Program terminated!")
    
