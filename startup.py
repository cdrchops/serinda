import os
import webbrowser
from sys import platform

# os.system("sh ./compileRust.sh")
# os.system("compileRust.bat")

# os.system("sh ./test.sh")
# os.system("test.bat")

from serinda.constants.ApplicationConstants import ApplicationConstants

# START OF SNIPS CODE

# from serinda.util.MergeCommandFiles import MergeCommandFiles

# merge all command files into one file
# MergeCommandFiles().mergeFiles()

# running snips this way generates a utf-8 file
# os.system("snips-nlu generate-dataset en " + ApplicationConstants.serindaCommandsYmlFile + " > " + ApplicationConstants.serindaCommandsJsonFile)

# if there is a utf-16 file then these next three commands would need to run
# os.system("python3 ./serinda/util/FileUtil.py")
# os.system("rm ./intents/serindaCommands.json")
# os.system("cp ./intents/serindaCommands2.json ./intents/serindaCommands.json")

#END OF SNIPS CODE

# determine os and installation
url = "http://localhost:8000"
browser = ""
if platform == "linux" or platform == "linux2":
    print("nothing here yet")
elif platform == "darwin":
    browser = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"
    webbrowser.get("open -a" + browser + " %s").open(url)
elif platform == "win32":
    # browser = 'C:/"Program Files (x86)"/Google/Chrome/Application/chrome.exe'
    os.system("start chrome " + url)

# this starts up the app and you get console logging just the same
os.system("python3 main.py --ip 0.0.0.0 --port 8000")

