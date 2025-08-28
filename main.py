from flask import Flask, render_template, request, jsonify, json, make_response, Response, send_from_directory
# some code from https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/

from flask_cors import CORS, cross_origin

import jinja2

from serinda.util.CommandProcessor import CommandProcessor
from serinda.util.PropertiesFile import PropertiesFile

from serinda.opencv.camerapool import CameraPool
import os
from pathlib import Path

app = Flask(__name__)

# CORS this is specifically for displaying PDFs - DO NOT USE THIS IN PRODUCTION
# this is meant to run on a local server not accessible by others - if you use this it can be exploited
CORS(app)

# to include multiple template paths
# https://buxty.com/b/2012/05/custom-template-folders-with-flask/
my_loader = jinja2.ChoiceLoader([app.jinja_loader, jinja2.FileSystemLoader('./')])
app.jinja_loader = my_loader

# populate all of the plugins for use on the index.html page
pluginTemplatePaths = []
pluginJavascriptPaths = []
pluginMenuPaths = []
indexParams = []
WAKE = "bob"


def determinePath(path):
    pathz = "/" + str(path)
    pathz = pathz.replace("\\", "/")

    return pathz


def populatePluginList(lst, pathlist):
    for path in pathlist:
        pathz = determinePath(path)
        lst.append(pathz)


populatePluginList(pluginTemplatePaths, Path("./serinda/plugin").glob('**/template.html'))
populatePluginList(pluginJavascriptPaths, Path("./serinda/plugin").glob('**/javascript.js'))
populatePluginList(pluginMenuPaths, Path("./serinda/plugin").glob('**/menu.html'))

propertiesFile = PropertiesFile()
commandProcessor = CommandProcessor(propertiesFile.get('nluFactory'))
cameraPool = CameraPool(propertiesFile)

messages = []

@app.route('/')
def index():
    return render_template('index.html',
                           cameraTotal=cameraPool.numberOfCameras,
                           pathList=pluginTemplatePaths,
                           javascriptList=pluginJavascriptPaths,
                           menuList=pluginMenuPaths)

@app.route('/file/', methods=['GET'])
def get_file(path=''):
    txt = Path('file://c:/projects/obsidianSync/reports/25Apr24.md').read_text()
    return txt

@app.route('/cmd')
def cmd():
    text = request.args.get('command', "", type=str)
    commandProcessor.processCommand2(cameraPool, text)
    return jsonify(result="success", status="success")

@app.route('/video_feed')
def video_feed():
    cameraNumber = request.args.get("id", "", type=int)
    return Response(cameraPool.getCamera(cameraNumber).generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stream')
def stream():
    return Response(commandProcessor.processCommand(request, cameraPool), mimetype="text/event-stream")

@app.route("/dofdata", methods=['GET', 'POST'])
def dofdata():
    gyrox = request.args.get("gyrox", 0, type=float)
    gyroy = request.args.get("gyroy", 0, type=float)
    gyroz = request.args.get("gyroz", 0, type=float)
    accelx = request.args.get("accelx", 0, type=float)
    accely = request.args.get("accely", 0, type=float)
    accelz = request.args.get("accelz", 0, type=float)
    magx = request.args.get("magx", 0, type=float)
    magy = request.args.get("magy", 0, type=float)
    magz = request.args.get("magz", 0, type=float)

    # messages.append("gyrox={0:0.3f}&gyroy={0:0.3f}&gyroz={0:0.3f}&accelx={0:0.3f}&accely={0:0.3f}&accelz={0:0.3f}&magx={0:0.3f}&magy={0:0.3f}&magz={0:0.3f}".format(gyrox, gyroy, gyroz, accelx, accely, accelz, magx, magy, magz))
    msg = "{"
    msg += "\"gyrox\":\"{0:0.3f}\"".format(gyrox)
    msg += ",\"gyroy\":\"{0:0.3f}\"".format(gyroy)
    msg += ",\"gyroz\":\"{0:0.3f}\"".format(gyroz)
    msg += ",\"accelx\":\"{0:0.3f}\"".format(accelx)
    msg += ",\"accely\":\"{0:0.3f}\"".format(accely)
    msg += ",\"accelz\":\"{0:0.3f}\"".format(accelz)
    msg += ",\"magx\":\"{0:0.3f}\"".format(magx)
    msg += ",\"magy\":\"{0:0.3f}\"".format(magy)
    msg += ",\"magz\":\"{0:0.3f}\"".format(magz)
    msg += "}"
    messages.append(msg)

    return jsonify(result="success", status="success")

@app.route('/listen', methods=['GET'])
def listen():
    def stream():
        # messages = listen()  # returns a queue.Queue
        while True:
            if len(messages):
                for message in messages:
                    # print(message)
                    yield 'data:{}\n\n'.format("text= " + message)
                    messages.remove(message)

    return Response(stream(), mimetype='text/event-stream')

if __name__ == '__main__':
    #create_app() -- for testing
    app.run(host='0.0.0.0', port='8000', debug=True)
    # working jpype with Java and Groovy
    # https://stackoverflow.com/questions/60964308/call-java-method-in-python-with-jpype
    # startJVM("-ea", classpath=[propertiesFile.get('groovyJar'), propertiesFile.get('javaFilePath')])
    # JavaTest = JClass("com.serinda.groovytest.JavaTest")
    #
    # JavaTest.printOut()
    #
    # GroovyTest = JClass("GroovyTest")
    #
    # GroovyTest.printOutTestString()
    # java.lang.System.out.println("hello world")

# shutdownJVM()
# deactivate the virtual environment
# os.system("deactivate")