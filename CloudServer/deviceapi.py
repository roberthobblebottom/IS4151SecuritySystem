from flask import Blueprint, render_template, request
import mysql.connector

deviceapi_blueprint = Blueprint('deviceapi_blueprint', __name__)

@deviceapi_blueprint.route("/available/<edge>")
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

@deviceapi_blueprint.route("/available")
def set_available_ipaddress():
    print("Set Available Called")
    conn = mysql.connector.connect(
	    host='localhost',
	    user='root',
	    passwd='password',
	    database='shs'
    )
    address = request.remote_addr
    update_status = "UPDATE edgeconnectors SET status = 1 WHERE ipaddress = %s"
    cur = conn.cursor()
    cur.execute(update_status, (address,))
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


@deviceapi_blueprint.route("/unavailable")
def set_unavailable_ipaddress():
    print("Set Available Called")
    conn = mysql.connector.connect(
	    host='localhost',
	    user='root',
	    passwd='password',
	    database='shs'
    )
    address = request.remote_addr
    update_status = "UPDATE edgeconnectors SET status = 0 WHERE ipaddress = %s "
    cur = conn.cursor()
    cur.execute(update_status, (address))
    conn.commit()
    cur.close()

    return "OK", 200

@deviceapi_blueprint.route("/unavailable/<edge>")
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