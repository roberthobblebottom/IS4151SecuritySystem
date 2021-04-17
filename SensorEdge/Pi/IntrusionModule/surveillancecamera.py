import time
from datetime import datetime
import picamera
from queue import Queue
import sqlite3
import serial
import socket
from threading import Thread
import requests
import io

filePath = '/home/pi/Documents/projectgg/files'

stop = False

# DB_NAME
DB_NAME = 'shs'

#Queues
queue = Queue()
queue2 = Queue()




def handleMessage(smsg):
    params = smsg.split()
    if params[1] == "int":
        queue2.put("record")
#         print("taking video")
#         fileName =  datetime.now().strftime("%Y%m%d%H%M%S") + '.h264'
#         camera.start_recording(filePath + "/" + fileName)
#         time.sleep(5)
#         camera.stop_recording()
#         curr = conn.cursor()
#         curr.execute("INSERT INTO intrusions (edgeconnector, videofile) VALUES (?,?)", (int(params[0]), fileName))
#         conn.commit()
#         curr.close()
#         print("Intrusion Detected, Video File:", fileName)
        
def videoCamera():
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 30
        camera.rotation = 90
        stream = picamera.PiCameraCircularIO(camera, seconds=20)
        camera.start_recording(stream, format='h264')
        try:
            while not stop:
                camera.wait_recording(1)
                while not queue2.empty():
                    param2 = queue2.get()
                    if param2 == "record":
                        print("Intrusion Detected, Recording")
                        # Keep recording for 10 seconds and only then write the
                        # stream to disk
                        camera.wait_recording(10)
                        write_video(stream)
        finally:
            camera.stop_recording()
        
def write_video(stream):
    print('Writing video!')
    with stream.lock:
        # Find the first header frame in the video
        for frame in stream.frames:
            if frame.frame_type == picamera.PiVideoFrameType.sps_header:
                stream.seek(frame.position)
                break
        # Write the rest of the stream to disk
        fileName =  datetime.now().strftime("%Y%m%d%H%M%S") + '.h264'
        with io.open(filePath + "/" + fileName, 'wb') as output:
            output.write(stream.read())
            print("File Complete! Written to", fileName)
            conn2 = sqlite3.connect(DB_NAME)
            curr = conn2.cursor()
            curr.execute("INSERT INTO intrusions (edgeconnector, videofile) VALUES (?,?)", (1, fileName))
            conn2.commit()
            curr.close()
            conn2.close()

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
        queue.put(message)
        client_socket.close()
        
def sendSettings():
    print("Settings called")
    #Connection to DB
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT globalalarmtime, forcedalarmtime, motiondetection FROM settings ORDER by updated DESC LIMIT 1")
    results = cur.fetchall()[0]
    print (results[0], results[1], results[2])
    ser.write(str.encode("gad$"+str(results[0])+"\r\n"))
    time.sleep(0.2) #wait for everything to send
    ser.write(str.encode("fad$"+str(results[1])+"\r\n"))
    time.sleep(0.2)
    ser.write(str.encode("md$"+str(results[2])+"\r\n"))
    time.sleep(0.2)

def serialListener():
    state = 0
    print("Telling Cloud we are available")
    result = requests.get("http://192.168.1.110:5000/api/available")
    globalalarmduration = result.json().get("globalalarmduration")
    print("Global Alarm:",globalalarmduration)
    ser.write(str.encode("gad$"+globalalarmduration+"\r\n"))
    time.sleep(0.2) #wait for everything to send
    forcedalarmduration = result.json().get("forcedalarmduration")
    print("Forced Alarm:",forcedalarmduration)
    ser.write(str.encode("fad$"+forcedalarmduration+"\r\n"))
    time.sleep(0.2)
    motiondetection = result.json().get("motiondetection")
    print("Motion Detection:",motiondetection) 
    ser.write(str.encode("md$"+motiondetection+"\r\n"))
    time.sleep(0.2)
    state = result.json().get("status")
    print(state)
    if state == 0:
        ser.write(str.encode("arm$0\r\n"))
    elif state == 1:
        ser.write(str.encode("unarm$1\r\n"))
    
    while not stop:
        while not queue.empty():
            param = queue.get()
            if param == "arm":
                state = 0
                print("arm called")
                ser.write(str.encode("arm$0\r\n"))
            elif param == "unarm":
                state = 1
                print("unarm called")
                ser.write(str.encode("unarm$1\r\n"))
            elif param == "alarm":
                print("alarm called")
                ser.write(str.encode("alarm$2\r\n"))
            elif param == "setting":
                sendSettings()
        if state == 0:
            lines = ser.readlines()
            if lines:
                for line in lines:
                   smsg = line.decode("utf-8").strip()
                   if len(smsg) > 0:
                       handleMessage(smsg) 


try:
    print("Camera Online")

    print("Listening on /dev/ttyACM0... Press CTRL+C to exit")
    print("Also listening on port 6789 for web services")
    
    ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1)
    #ser.write(str.encode("test\r\n"))
    t1 = Thread(target = videoCamera)
    t2 = Thread(target = socketListener)
    t1.setDaemon(True)
    t2.setDaemon(True)
    t1.start()
    t2.start()
    serialListener()
except KeyboardInterrupt:
    stop = True
    if ser.is_open:
        ser.write(str.encode("shutdown$2\r\n"))
        ser.close()
    # conn.close()
    print("Program terminated!")
finally:
    print("Cleaning Up")
    result = requests.get("http://192.168.1.110:5000/api/unavailable")
    
