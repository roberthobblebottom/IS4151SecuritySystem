from flask import Blueprint, render_template
import mysql.connector

device_blueprint = Blueprint('device_blueprint', __name__)

# This component contains functionalities for devices

@device_blueprint.route("/devicepanel")
def devicepanel():
    conn = mysql.connector.connect(
	    host='localhost',
	    user='root',
	    passwd='password',
	    database='shs'
    )
    cur = conn.cursor()
    sql = "SELECT edgeconnectors.*, devicetype.devicetype FROM edgeconnectors JOIN devicetype on edgeconnectors.devicetype = devicetype.id;"
    cur.execute(sql)
    devices = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("devicepanel.html", devices=devices)

@device_blueprint.route("/devices")
def devices_screen():
    conn = mysql.connector.connect(
	    host='localhost',
	    user='root',
	    passwd='password',
	    database='shs'
    )
    cur = conn.cursor()
    sql = "SELECT edgeconnectors.*, devicetype.devicetype FROM edgeconnectors JOIN devicetype on edgeconnectors.devicetype = devicetype.id"
    cur.execute(sql)
    devices = cur.fetchall()
    sql = "SELECT * FROM devicetype"
    cur.execute(sql)
    devicetypes = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template("devices.html", devices=devices, devicetypes=devicetypes)

@device_blueprint.route("/adddevice", methods=["POST"])
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
    sql = "INSERT INTO edgeconnectors (edgename, ipaddress, devicetype, status) VALUES (%s, %s, %s, 0)"
    cur.execute(sql, (name,ipaddress,devicetype,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/devices")

@device_blueprint.route("/deletedevice/<id>")
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

@device_blueprint.route("/editdevice", methods=["POST"])
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
    sql = "UPDATE edgeconnectors SET edgename = %s, ipaddress = %s, devicetype = %s WHERE id = %s"
    cur.execute(sql, (name,ipaddress,devicetype,did,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/devices")