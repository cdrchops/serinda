import os
import webbrowser
from sys import platform
from enum import Enum #to do enum work in this file - overkill? maybe, but I want to do it this way... for now 9Mar24 wink
from serinda.constants.ApplicationConstants import ApplicationConstants
from serinda.util.MergeCommandFiles import MergeCommandFiles

class Platform(Enum):
    UNDEFINED = 0
    LINUX = 1
    MAC = 2
    WINDOWS = 3

PLATFORM = Platform.UNDEFINED

if platform == "linux" or platform == "linux2":
    PLATFORM = Platform.LINUX
elif platform == "darwin":
    PLATFORM = Platform.MAC
elif platform == "win32":
    PLATFORM = Platform.WINDOWS

if PLATFORM == Platform.LINUX:
    os.system("source /mnt/c/projects/debvenv/env/bin/activate")
# elif PLATFORM == Platform.WINDOWS:
#     print("right here")
#     #c:\\projects\\serinda\\serindaMain\\
#     os.system("c:\\projects\\venv\\Scripts\\activate")

# merge all command files into one file
MergeCommandFiles().mergeFiles()

# running snips this way generates a utf-8 file
os.system("snips-nlu generate-dataset en " + ApplicationConstants.serindaCommandsYmlFile + " > " + ApplicationConstants.serindaCommandsJsonFile)

# TODO: maybe make this a property instead of OS dependent
PYTHON_NAME = "python" if PLATFORM == Platform.WINDOWS else "python3"

OS_DELETE_COMMAND = "rm"
OS_COPY_COMMAND = "cp"

if PLATFORM == Platform.WINDOWS:
    OS_DELETE_COMMAND = "del"
    OS_COPY_COMMAND = "copy"

#TODO: make these paths os independent
os.system(OS_DELETE_COMMAND + " " + os.path.join("intents", "serindaCommands.json"))
os.system(OS_COPY_COMMAND + " " + os.path.join("intents", "serindaCommands2.json") + " " + os.path.join("intents", "serindaCommands.json"))
# the intent behind this next file is in the header of it - for now I'm commenting it out as it doesn't appear to be needed
#     on windows
# os.system(PYTHON_NAME + " .\\serinda\\util\\FileUtil.py")

# determine os and installation
url = "http://localhost:8000"
browser = ""
if PLATFORM == Platform.LINUX:
    # os.system("sh ./compileRust.sh")
    # os.system("sh ./test.sh")
    print("nothing here yet")
elif PLATFORM == Platform.MAC:
    # os.system("sh ./compileRust.sh")
    # os.system("sh ./test.sh")
    browser = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"
    webbrowser.get("open -a" + browser + " %s").open(url)
elif PLATFORM == Platform.WINDOWS:
    os.system("compileRust.bat")
    os.system("test.bat")
    # browser = 'C:/"Program Files (x86)"/Google/Chrome/Application/chrome.exe'
    os.system("start chrome " + url)
    # print("nothing here yet")

# this starts up the app and you get console logging just the same
os.system("python main.py --ip 0.0.0.0 --port 8000")