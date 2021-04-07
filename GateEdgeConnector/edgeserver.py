import serial
import time
import sqlite3
import requests
import json
import socket
from threading import Thread, Lock
from queue import Queue

DB_NAME = "CloudSecure"

#Connection to DB
conn = sqlite3.connect(DB_NAME)

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
        # Handle Messages
        client_socket.close()

def serialListener():
    while not stop:
        while not queue.empty()
            message = queue.get()
            # handle messages
    
    #Serial Communication

try:
    queue = Queue()
    ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1)
    thread = Thread(target = socketListener)
    thread.setDaemon(True)
    thread.start()
    serialListener()
    while True:
        pass
except KeyboardInterrupt:
    stop = True
    if ser.is_open:
        ser.close()
    RedLed.off()
    conn.close()
    print("Program terminated!")