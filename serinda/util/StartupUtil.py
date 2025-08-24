from pathlib import Path

from serinda.util.PropertiesFile import PropertiesFile

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful for multiple browsers/tabs
# are viewing
# the stream)
# from serinda.translations.TranslationMatrix import TranslationMatrix
from serinda.opencv.camerapool import CameraPool

# from jpype import *

from serinda.util.CommandProcessor import CommandProcessor

class StartupUtil:
    # populate all of the plugins for use on the index.html page
    pluginTemplatePaths = []
    pluginJavascriptPaths = []
    pluginMenuPaths = []

    indexParams = []

    def __init__(self):
        self.populatePluginList(self.pluginTemplatePaths, Path("./serinda/plugin").glob('**/template.html'))
        self.populatePluginList(self.pluginJavascriptPaths, Path("./serinda/plugin").glob('**/javascript.js'))
        self.populatePluginList(self.pluginMenuPaths, Path("./serinda/plugin").glob('**/menu.html'))
        # self.indexParams = cameraTotal=self.cameraPool.numberOfCameras, pathList=self.pluginTemplatePaths, javascriptList=self.pluginJavascriptPaths, menuList=self.pluginMenuPaths
        self.commandProcessor = CommandProcessor()
        self.propertiesFile = PropertiesFile()
        self.cameraPool = CameraPool(self.propertiesFile)

    def determinePath(self, path):
        pathz = "/" + str(path)
        pathz = pathz.replace("\\", "/")

        return pathz

    def populatePluginList(self, lst, pathlist):
        for path in pathlist:
            pathz = self.determinePath(path)
            lst.append(pathz)

    # matches app.py cmd
    def cmd(self, request):
        text = request.args.get('command', "", type=str)
        self.commandProcessor.processCommand2(self.cameraPool, text)

    # matches app.py video_feed
    def videoFeed(self, request):
        cameraNumber = request.args.get("id", "", type=int)
        return self.cameraPool.getCamera(cameraNumber)

    def stream(self, request):
        return self.commandProcessor.processCommand(self.cameraPool)