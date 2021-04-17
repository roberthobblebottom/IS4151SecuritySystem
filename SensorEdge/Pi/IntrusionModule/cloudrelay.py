import time
import sqlite3
import requests
import json
from subprocess import call

filePath = '/home/pi/Documents/projectgg/files'
EDGE_CONNECTOR_NAME = "surveillancecamera"

try:
    conn = sqlite3.connect('shs')

    #base_uri = 'http://169.254.78.152:5000/'
    # base_uri = 'http://192.168.18.13:5000/upload'
    base_uri = 'http://192.168.1.110:5000/upload'
    test_uri = 'http://httpbin.org/post'
    while True:
        time.sleep(8)
        print('Relaying data to cloud server...')
        c = conn.cursor()
        c.execute("SELECT rowid, edgeconnector, videofile FROM intrusions WHERE uploaded = 0")
        results = c.fetchall()
        
        for result in results:
            # file = open(filePath + "/" + result[2], "rb")
            print("Processing", result[2])
            file_convert = filePath + "/" + result[2]
            final_file = file_convert + "_.mp4"
            command = "MP4Box -add " + file_convert + " " + final_file
            call([command], shell = True)
            print("Converted! Uploading...")
            file = open(final_file, "rb")
            test_response = requests.post(base_uri + "/1" , files={"file": file})
            print(test_response)
            c = conn.cursor()
            c.execute("UPDATE intrusions SET uploaded = 1 WHERE rowid = ?", (int(result[0]),))
            conn.commit()
        
        
        c.close()
        
except KeyboardInterrupt:
	
	print('********** END')
	
except Error as err:

	print('********** ERROR: {}'.format(err))

finally:

	conn.close()