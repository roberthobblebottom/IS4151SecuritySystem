from flask import Flask, render_template, request, make_response, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import mysql.connector
import json
import string
import requests
import random
from twilio.rest import Client
import config
from devices import device_blueprint
from intrusions import intrusion_blueprint
from deviceapi import deviceapi_blueprint
 

twilio_client = Client(config.account_sid, config.auth_token) 
app = Flask(__name__)
app.static_folder = './'
app.config['UPLOAD_FOLDER'] = "/files"
headers = {'content-type' : 'application/json'}
app.register_blueprint(device_blueprint)
app.register_blueprint(intrusion_blueprint)
app.register_blueprint(deviceapi_blueprint, url_prefix="/api")


@app.route("/upload/<edgeconnector>", methods=['POST'])
def upload_file(edgeconnector):
    f = request.files['file']
    f.save(secure_filename(f.filename))
    conn = mysql.connector.connect(
		host='localhost',
		user='root',
		passwd='password',
		database='shs'
	)
    address = request.remote_addr
    curr = conn.cursor()
    up= "UPDATE edgeconnectors SET ipaddress = %s WHERE id = %s"
    curr.execute(up, (address, int(edgeconnector)))
    sql = """INSERT INTO unauthentry(edgeconnector, datetime, file) VALUES (%s,NOW(),%s)"""
    curr.execute(sql, (int(edgeconnector), f.filename,))
    conn.commit()
    curr.close()
    conn.close()
    message = twilio_client.messages.create(  
                              messaging_service_sid='MG1a02ec809a4c9a3c2ed93602b019a065', 
                              body='[SimpleHomeSecure] There is a potential intrusion from ' + edgeconnector + '! Click on the link to take a look. http://192.168.1.110:5000',      
                              to='+6593673358' 
                          ) 
 
    print(message.sid)

    return make_response('Records successfully created', 200)

@app.route("/auth", methods=['GET'])
def create_auth_code():
    # generates an authentication code and stores it in the database, then returns the auth as a json object
    conn = mysql.connector.connect(
		host='localhost',
		user='root',
		passwd='password',
		database='shs'
	)
    letters = string.ascii_letters
    password = ''.join(random.choice(letters) for i in range(16))

@app.route("/")
def index():
    conn = mysql.connector.connect(
	    host='localhost',
	    user='root',
	    passwd='password',
	    database='shs'
    )
    cur = conn.cursor()
    sql = "SELECT edgename, ipaddress, devicetype FROM edgeconnectors WHERE devicetype = 2 or devicetype = 3"
    cur.execute(sql)
    results = cur.fetchall()
    # get camera streams 
    cur.close()
    conn.close()
    return render_template("index.html", cameras=results)

@app.route("/statusbutton")
def statusbutton():
    conn = mysql.connector.connect(
	    host='localhost',
	    user='root',
	    passwd='password',
	    database='shs'
    )
    cur = conn.cursor()
    sql= "SELECT statusnumber FROM status ORDER by statusdate DESC LIMIT 1"
    cur.execute(sql)
    results = cur.fetchall()
    statusnumber = results[0][0]
    cur.close()
    conn.close()
    return render_template("statusbutton.html", status=statusnumber)




@app.route("/unlock")
def unarm_system():
    conn = mysql.connector.connect(
	    host='localhost',
	    user='root',
	    passwd='password',
	    database='shs'
    )
    cur = conn.cursor()
    sql = "INSERT INTO status (statusnumber) VALUES (1)"
    cur.execute(sql)
    conn.commit()
    cur = conn.cursor()
    sql = "SELECT ipaddress, devicetype from edgeconnectors WHERE status = 1 AND (devicetype = 1 or devicetype = 2)"
    cur.execute(sql)
    addresses = cur.fetchall()
    conn.close()
    for address in addresses:
        if address[1] == 1:
            response = requests.post("http://" + address[0] + ":5000/api/status/1")
        elif address[1] == 2:
            response = requests.post("http://" + address[0] + ":5000/unarm")
    return statusbutton()

@app.route("/lock")
def arm_system():
    conn = mysql.connector.connect(
	    host='localhost',
	    user='root',
	    passwd='password',
	    database='shs'
    )
    cur = conn.cursor()
    sql = "INSERT INTO status (statusnumber) VALUES (0)"
    cur.execute(sql)
    conn.commit()
    cur.close()
    cur = conn.cursor()
    sql = "SELECT ipaddress, devicetype from edgeconnectors WHERE status = 1 AND (devicetype = 1 or devicetype = 2)"
    cur.execute(sql)
    addresses = cur.fetchall()
    conn.close()
    for address in addresses:
        if address[1] == 1:
            response = requests.post("http://" + address[0] + ":5000/api/status/0")
        elif address[1] == 2:
            response = requests.post("http://" + address[0] + ":5000/arm")

    return statusbutton()



@app.route("/startalarm/<edgeconnector>")
def start_alarm(edgeconnector):
    # Alarm tentatively only lasts for 5s
    conn = mysql.connector.connect(
	    host='localhost',
	    user='root',
	    passwd='password',
	    database='shs'
    )
    cur = conn.cursor()
    sql = 'SELECT ipaddress from edgeconnectors WHERE id = %s'
    cur.execute(sql, (int(edgeconnector),))
    results = cur.fetchall()
    ipaddress = results[0][0]
    response = requests.post("http://" + ipaddress + ":5000/api/status/2")
    return "OK", 200




# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)