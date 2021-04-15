import connexion
import sqlite3
import socket
from flask import make_response

app = connexion.App(__name__, specification_dir='./')
app.add_api('edge.yml')

edge_connector = "Camera"

@app.route('/')
def index():
	
	return "Hello World"



# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
