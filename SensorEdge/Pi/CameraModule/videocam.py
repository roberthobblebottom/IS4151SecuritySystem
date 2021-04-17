from flask import Flask, Response
from queue import Queue
from camera_pi import Camera
import sqlite3
import requests
import setup

app = Flask(__name__)
instructionQueue = Queue()

active = False

DB_NAME = 'shscamera'

#Base Generator Idea found from Guide: https://blog.miguelgrinberg.com/post/video-streaming-with-flask. Modified for use with SHS

def gen(camera):
    """Video streaming generator function."""
    while True:
        #Breaks if Deactivated
        while not instructionQueue.empty():
            param = instructionQueue.get()
            if (param == "end"):
                return
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video')
def video_feed():
    conn = sqlite3.connect(DB_NAME)
    curr = conn.cursor()
    curr.execute("SELECT status FROM armstatus ORDER BY timestmp DESC LIMIT 1")
    active = curr.fetchall()[0][0]
    print(active)
    if active == 0:
        return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return "ERROR", 500

@app.route('/unarm', methods= ["POST"])
def unarm():
    print("Unarming and stopping stream")
    instructionQueue.put("end")
    conn = sqlite3.connect(DB_NAME)
    curr = conn.cursor()
    curr.execute("INSERT INTO armstatus (status) VALUES (1)")
    conn.commit()
    curr.close()
    conn.close()
    return "OK", 200
    
@app.route('/arm', methods = ["POST"])
def arm():
    print("Arming and activating stream")
    conn = sqlite3.connect(DB_NAME)
    curr = conn.cursor()
    curr.execute("INSERT INTO armstatus (status) VALUES (0)")
    conn.commit()
    curr.close()
    conn.close()
    return "OK", 200

if __name__ == '__main__':
    # get initial setup
    setup.setup_device()
    initialStatusJson = requests.get("http://192.168.1.110:5000/available")
    initialStatus = initialStatusJson.json().get("status")
    conn = sqlite3.connect(DB_NAME)
    curr = conn.cursor()
    curr.execute("INSERT INTO armstatus (status) VALUES (?)", (initialStatus,))
    conn.commit()
    curr.close()
    conn.close()
    
    app.run(host='0.0.0.0', port=5000, threaded=True)