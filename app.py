from flask import Flask, render_template
from packageParser import parse_packages

app = Flask(__name__)
packages, realFile = parse_packages()

@app.route('/')
def index():
    global packages
    global realFile
    return render_template('index.html', packages=sorted(packages), realFile=realFile)

@app.route('/details/<string:name>')
def details(name):
    global packages
    return render_template('details.html', name=name, packages=packages, details=packages[name])

@app.errorhandler(404)
def page_not_found(e):
    return "There's nothing for you here", 404

@app.errorhandler(500)
def page_not_found(e):
    return "Something went wrong, apologies", 500

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
