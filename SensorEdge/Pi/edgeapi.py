import sqlite3
from flask import make_response
import socket

EDGE_CONNECTOR = "CameraEdge"

# def emergency(edgeconnector):
#     if edgeconnector != EDGE_CONNECTOR:
#         print("starting emergency")
#         host = socket.gethostname()
#         port = 6789
#         s = socket.socket()
#         s.connect((host, port))
#         message = "globalemergency"
#         s.send(message.encode("utf-8"))
#         s.close()
#     else:
#         print("its actually local")
#     return make_response('Message Sent', 200)

# def stopemergency():
#     host = socket.gethostname()
#     port = 6789
#     s = socket.socket()
#     s.connect((host, port))
#     message = "stopemergency"
#     s.send(message.encode("utf-8"))
#     s.close()
#     return make_response('Alarm Stopped', 200)

def status(statusNumber):
    host = socket.gethostname()
    port = 6789
    s = socket.socket()
    s.connect((host, port))
    if status == 0:
        message = "arm"
        s.send(message.encode("utf-8"))
        s.close()
        return make_response("Armed", 200)
    elif status == 1:
        message = "unarm"
        s.send(message.encode("utf-8"))
        s.close()
        return make_response("Unarmed", 200)
    else
        return make_response("Error", 400)