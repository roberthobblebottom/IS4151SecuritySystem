import connexion
from flask import render_template,request,url_for,redirect
import secrets
import os
toggle = False
app = connexion.App(__name__, specification_dir='./')
secret =  secrets.token_urlsafe(32)
app.secret_key = secret
#app.add_api('swagger.yml')
# app.add_api('swaggerfull.yml')

@app.route('/')
def index():
  os.system("python databaseInit.py")
  return render_template('login.html')

@app.route('/login',methods=["POST"])
def login():
  if request.method == "POST":
    username = request.form.get("uname")
    password = request.form.get("psw")
    if username == "user" and password == "password": 
      return redirect(url_for("dashboard", loginSuccess = True))
    else :
      return render_template("login.html",result="login failed")
@app.route('/dashboard/<loginSuccess>')
def dashboard(loginSuccess):
   if loginSuccess:
      print("LoginSuccess string")
      return render_template("dashboard.html",loginSuccess = "Logged in successfully.",
      toggleSecurityMode = "Activate Security") 
   else: 
     print("loginSuccess string gone")
     return render_template("dashboard.html") 

@app.route('/dashboard', methods={"POST"})
def toggleAlarmInDashBoard():
  toggle = not toggle
  if toggle:
    print("toggle: true")
    return render_template("dashboard.html",toggleSecurityMode = "Deactivate Security")
  elif not toggle:
    print("toggle false")
    return render_template("dashboard.hmtl",toggleSecurityMode = "Activate Security")

@app.route('/toggle',methods={"post"})
def toggleButton():
    return redirect(url_for("dashboard"))
# If we're running in stand alone mode, run the application
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000, debug=True)
