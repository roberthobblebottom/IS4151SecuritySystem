import connexion

app = connexion.App(__name__, specification_dir='./')
app.app.config['UPLOAD_FOLDER'] = "/files"
headers = {'content-type' : 'application/json'}

@app.route("/upload", methods=['POST'])
def upload_file():
    from werkzeug.datastructures import FileStorage
    FileStorage(request.stream).save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return 'OK', 200

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)