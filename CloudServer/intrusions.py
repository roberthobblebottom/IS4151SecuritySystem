from flask import Blueprint, render_template
import mysql.connector

intrusion_blueprint = Blueprint('intrusion_blueprint', __name__)

@intrusion_blueprint.route("/latestintrusions")
def get_latest_intrusions():
    conn = mysql.connector.connect(
	    host='localhost',
	    user='root',
	    passwd='password',
	    database='shs'
    )
    cur = conn.cursor()
    sql = "SELECT i.id, e.edgename, DATE_FORMAT(i.datetime,'%e %b %Y %h:%i %p') as date, i.file FROM unauthentry i JOIN edgeconnectors e ON (i.edgeconnector = e.id) WHERE i.datetime > DATE_SUB(NOW(), INTERVAL '3' HOUR)"
    cur.execute(sql)
    intrusions = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("intrusionpanel.html", intrusions=intrusions)

@intrusion_blueprint.route("/intrusions")
def get_intrusions():
    conn = mysql.connector.connect(
	    host='localhost',
	    user='root',
	    passwd='password',
	    database='shs'
    )
    cur = conn.cursor()
    sql = "SELECT i.id, e.edgename, DATE_FORMAT(i.datetime,'%e %b %Y %h:%i %p') as date, i.file, e.id FROM unauthentry i JOIN edgeconnectors e ON (i.edgeconnector = e.id) ORDER BY i.datetime DESC"
    cur.execute(sql)
    intrusions = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("intrusions.html", intrusions=intrusions)
