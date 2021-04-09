import connexion
import sqlite3
import socket
from flask import make_response

app = connexion.App(__name__, specification_dir='./')
app.add_api('edge.yml')

edge_connector = "Camera"

@app.route('/')
def index():

# 	conn = sqlite3.connect('firyeedge')
# 	c = conn.cursor()
# 	c.execute('select s.device, s.temperature, s.light, s.sensorDate FROM sensordata s INNER JOIN (select device, max(sensordate) as maxdate from sensordata group by device) s1 on s.device = s1.device and s.sensorDate = s1.maxdate where s.sensordate = s1.maxdate order by s.device ASC;')
# 	results = c.fetchall()
# 	
# 	html = '<html><head><title>Edge1</title></head><body><h1>Local Values</h1><table cellspacing="1" cellpadding="3" border="1"><tr><th>Device Name</th><th>Lastest Temperature</th><th>Lastest Light Level</th><th>Updated</th></tr>'
# 	for result in results:
# 				
# 		html += '<tr><td>' + str(result[0]) + '</td><td>' + str(result[1]) + '</td><td>' + str(result[2]) + '</td><td>' + result[3] + '</td></tr>'
# 	
# 	html += '</body></html>'
# 	
# 	conn.close()
	
	return "Hello World"

# @app.route('/emergency/<edgeconnector>')
# def setglobalemergency(edgeconnector):
#     host = socket.gethostname()
#     port = 6789
#     s = socket.socket()
#     s.connect((host, port))
#     if edgeconnector != edge_connector:
#         message = "globalemergency"
#         s.send(message.encode("utf-8"))
#     else:
#         message = "localemergency"
#         s.send(message.encode("utf-8"))
#     s.close()
#     return make_response('Alarm Sent', 200)



# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
