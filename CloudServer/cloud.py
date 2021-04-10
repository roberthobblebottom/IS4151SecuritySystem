import connexion
from flask import render_template, request, make_response
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import mysql.connector
import json
import string
import random

app = connexion.App(__name__, specification_dir='./')
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
		database='simplehomesecure'
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
		database='simplehomesecure'
	)
    letters = string.ascii_letters
    password = ''.join(random.choice(letters) for i in range(16))

@app.route("/")
def index():
    return "Hello World"


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)