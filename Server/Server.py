import connexion
from flask import render_template,request,url_for,redirect,session
import secrets
import os
import psycopg2
app = connexion.App(__name__, specification_dir='./')
secret =  secrets.token_urlsafe(32)
app.secret_key = secret
#app.add_api('swagger.yml')
# app.add_api('swaggerfull.yml')

@app.route('/')
def index():
  return render_template('login.html')

@app.route('/login',methods=["POST"])
def login():
  if request.method == "POST":
    username = request.form.get("uname")
    password = request.form.get("psw")
    mydb = psycopg2.connect(
      host='localhost',
      user='postgres',
      password='password',
      database='securitysystem'
    )
    mycursor = mydb.cursor()
    sql = """
           SELECT username,password,isAlarm FROM user1 WHERE username = %s AND password = %s;
          """
    query = (username,password)
    mycursor.execute(sql,query)
    result = mycursor.fetchone();
    print(result)
    if result is not None: 
      session['isLogin'] = True
      session['username'] = username
      session['isAlarm'] = result[2]
      print(session[isAlarm])
      return redirect(url_for("dashboard", loginSuccess = True))
    else :
      return render_template("login.html",result="login failed")
@app.route('/dashboard/<loginSuccess>')
def dashboard(loginSuccess):
   if loginSuccess:
      print("LoginSuccess string")
      return render_template("dashboard.html",
      loginSuccess = "Logged in successfully.",
      actionText = "Alarm is turned on.",
      toggleSecurityMode = "Activate Security") 
   else: 
     print("loginSuccess string gone")
     return render_template("dashboard.html") 
@app.route("/dashboard")
def toggleAlarmInDashboard():
  on = "Alarm is turned on."
  off = "Alarm is turned off"
  print(request.form.get("actionText"))
  if request.form.get("actionText") == on:
      print("toggle: true")
      return render_template("dashboard.html",
                              toggleSecurityMode = "Activate Security",
                              actionText = off)
  else:
      print("toggle false")
      return render_template("dashboard.html",
                            toggleSecurityMode = "Deactivate Security",
                            actionText= on)
  return render_template("dashboard.html",
                            toggleSecurityMode = request.form.get("toggleSecurityMode"),
                            actionText= request.form.get("actionText"))
@app.route('/toggle',methods={"post"})
def toggleButton():
    return redirect(url_for("toggleAlarmInDashboard"))
# If we're running in stand alone mode, run the application
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000, debug=True)
