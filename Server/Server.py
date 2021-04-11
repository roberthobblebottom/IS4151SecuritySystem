import connexion
from flask import render_template,request,url_for,redirect

app = connexion.App(__name__, specification_dir='./')

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
    print("Login credentials:")
    print(username)
    print(password)
    if username == "user" and password == "password": 
      print("login successful")
      return redirect(url_for("dashBoard"))
    else :
      print("login failed")

@app.route('/dashboard')
def dashBoard():
   return render_template("dashboard.html")

# If we're running in stand alone mode, run the application
if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)

