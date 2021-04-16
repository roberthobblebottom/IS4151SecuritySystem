from flask import Blueprint, render_template, redirect, request
import mysql.connector

settings_blueprint = Blueprint('settings_blueprint', __name__)

@settings_blueprint.route("/settings")
def settings_page():
    defaultalarmduration = 0
    forcedalarmduration = 0
    mobilenumber = ""
    movealarm = 0
    conn = mysql.connector.connect(
	    host='localhost',
	    user='root',
	    passwd='password',
	    database='shs'
    )
    cur = conn.cursor()
    sql= "SELECT * FROM settings"
    cur.execute(sql)
    settings = cur.fetchall()
    cur.close()
    conn.close()
    for setting in settings:
        if setting[0] == "defaultalarm":
            defaultalarmduration = int(setting[1])
        elif setting[0] == "forcedalarm":
            forcedalarmduration = int(setting[1])
        elif setting[0] == "mobilenumber":
            mobilenumber = setting[1]
        elif setting[0] == "movealarm":
            movealarm = int(setting[1]) 
    return render_template("settings.html", defaultalarmduration=defaultalarmduration, forcedalarmduration = forcedalarmduration, mobilenumber=mobilenumber, movealarm=movealarm)

@settings_blueprint.route("/editsettings", methods=["POST"])
def edit_settings():
    conn = mysql.connector.connect(
	    host='localhost',
	    user='root',
	    passwd='password',
	    database='shs'
    )
    defaultalarmduration = request.form["defaultalarmduration"]
    forcedalarmduration = request.form["forcedalarmduration"]
    mobilenumber = request.form["mobilenumber"]
    movealarm = request.form.getlist("movealarm")
    print(movealarm)

    curr = conn.cursor()
    sql = "UPDATE settings SET settingvalue = %s WHERE settingname = \"defaultalarm\""
    curr.execute(sql, (str(defaultalarmduration),))
    sql = "UPDATE settings SET settingvalue = %s WHERE settingname = \"forcedalarm\""
    curr.execute(sql, (str(forcedalarmduration),))
    sql = "UPDATE settings SET settingvalue = %s WHERE settingname = \"mobilenumber\""
    curr.execute(sql, (mobilenumber,))
    conn.commit()
    conn.close()
    return redirect("/settings?changed=true")