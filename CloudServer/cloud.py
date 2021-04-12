import connexion
from flask import render_template, request, make_response, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import mysql.connector
import json
import string
import requests
import random

app = connexion.App(__name__, specification_dir='./')
app.app.static_folder = './'
app.app.config['UPLOAD_FOLDER'] = "/files"
headers = {'content-type' : 'application/json'}

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
    sql = "SELECT edgename, ipaddress FROM edgeconnectors WHERE edgetype = 1"
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

@app.route("/devicepanel")
def devicepanel():
    conn = mysql.connector.connect(
	    host='localhost',
	    user='root',
	    passwd='password',
	    database='shs'
    )
    cur = conn.cursor()
    sql = "SELECT * FROM edgeconnectors"
    cur.execute(sql)
    devices = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("devicepanel.html", devices=devices)

@app.route("/latestintrusions")
def get_latest_intrusions():
    conn = mysql.connector.connect(
	    host='localhost',
	    user='root',
	    passwd='password',
	    database='shs'
    )
    cur = conn.cursor()
    sql = "SELECT e.id, e.edgename, DATE_FORMAT(i.datetime,'%e %b %Y %h:%i %p') as date, i.file FROM unauthentry i JOIN edgeconnectors e ON (i.edgeconnector = e.id) WHERE i.datetime > DATE_SUB(NOW(), INTERVAL '3' HOUR)"
    cur.execute(sql)
    intrusions = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("intrusionpanel.html", intrusions=intrusions)

@app.route("/intrusions")
def get_intrusions():
    conn = mysql.connector.connect(
	    host='localhost',
	    user='root',
	    passwd='password',
	    database='shs'
    )
    cur = conn.cursor()
    sql = "SELECT i.id, e.edgename, DATE_FORMAT(i.datetime,'%e %b %Y %h:%i %p') as date, i.file FROM unauthentry i JOIN edgeconnectors e ON (i.edgeconnector = e.id) ORDER BY i.datetime DESC"
    cur.execute(sql)
    intrusions = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("intrusions.html", intrusions=intrusions)

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
    sql = "SELECT ipaddress from edgeconnectors WHERE status = 1 AND edgetype = 0"
    cur.execute(sql)
    addresses = cur.fetchall()
    conn.close()
    for address in addresses:
        response = requests.post("http://" + address[0] + ":5000/api/status/1")
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
    sql = "SELECT ipaddress from edgeconnectors WHERE status = 1 AND edgetype = 0"
    cur.execute(sql)
    addresses = cur.fetchall()
    conn.close()
    for address in addresses:
        response = requests.post("http://" + address[0] + ":5000/api/status/0")

    return statusbutton()

@app.route("/available/<edge>")
def set_available(edge):
    print("Set Available Called")
    conn = mysql.connector.connect(
	    host='localhost',
	    user='root',
	    passwd='password',
	    database='shs'
    )
    address = request.remote_addr
    update_status = "UPDATE edgeconnectors SET status = 1, ipaddress = %s WHERE id = %s"
    cur = conn.cursor()
    cur.execute(update_status, (address,int(edge),))
    conn.commit()
    cur.close()

    #get status and return
    cur = conn.cursor()
    sql= "SELECT statusnumber FROM status ORDER by statusdate DESC LIMIT 1"
    cur.execute(sql)
    results = cur.fetchall()
    statusnumber = results[0][0]
    cur.close()
    conn.close()
    
    return { "status" : statusnumber }


@app.route("/devices")
def devices_screen():
    conn = mysql.connector.connect(
	    host='localhost',
	    user='root',
	    passwd='password',
	    database='shs'
    )
    cur = conn.cursor()
    sql = "SELECT * FROM edgeconnectors"
    cur.execute(sql)
    devices = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("devices.html", devices=devices)

@app.route("/unavailable/<edge>")
def set_unavailable(edge):
    print("Set Unavailable Called")
    conn = mysql.connector.connect(
	    host='localhost',
	    user='root',
	    passwd='password',
	    database='shs'
    )
    address = request.remote_addr
    update_status = "UPDATE edgeconnectors SET status = 0, ipaddress = %s WHERE id = %s"
    cur = conn.cursor()
    cur.execute(update_status, (address,int(edge),))
    conn.commit()
    cur.close()
    conn.close()

    return "OK", 200

@app.route("/adddevice", methods=["POST"])
def add_device():
    conn = mysql.connector.connect(
	    host='localhost',
	    user='root',
	    passwd='password',
	    database='shs'
    )
    name = request.form["newdevicename"]
    ipaddress= request.form["ipaddress"]
    devicetype = request.form["devicetype"]
    cur = conn.cursor()
    sql = "INSERT INTO edgeconnectors (edgename, ipaddress, edgetype, status) VALUES (%s, %s, %s, 0)"
    cur.execute(sql, (name,ipaddress,devicetype,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/devices")

@app.route("/deletedevice/<id>")
def delete_device(id):
    conn = mysql.connector.connect(
	    host='localhost',
	    user='root',
	    passwd='password',
	    database='shs'
    )
    cur = conn.cursor()
    sql = "DELETE FROM unauthentry WHERE edgeconnector = %s"
    cur.execute(sql,(int(id),))
    conn.commit()
    sql = "DELETE FROM edgeconnectors WHERE id = %s"
    cur.execute(sql,(int(id),))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/devices")

@app.route("/editdevice", methods=["POST"])
def edit_device():
    conn = mysql.connector.connect(
	    host='localhost',
	    user='root',
	    passwd='password',
	    database='shs'
    )
    did= request.form["editdeviceid"]
    name = request.form["editdevicename"]
    ipaddress= request.form["editipaddress"]
    devicetype = request.form["editdevicetype"]
    cur = conn.cursor()
    sql = "UPDATE edgeconnectors SET edgename = %s, ipaddress = %s, edgetype = %s WHERE id = %s"
    cur.execute(sql, (name,ipaddress,devicetype,did,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/devices")

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)