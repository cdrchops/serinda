# Alternate continuation project of snips-nlu https://github.com/jr-k/snips-nlu-rebirth
from snips_nlu import SnipsNLUEngine
import io
import json

from serinda.constants.ApplicationConstants import ApplicationConstants


class SnipsIntent:
    # specifically the fileOpen parameter is so that testing can adjust the path where this would normally
    # be the expected path - testing hardcoded paths requires them to go up a directory since the
    # TESTS directory is one down from the root directory
    def __init__(self, fileOpen = ApplicationConstants.serindaCommandsJsonFile):
        with io.open(fileOpen) as f:
            sample_dataset = json.load(f)

        self.nlu_engine = SnipsNLUEngine()
        self.nlu_engine.fit(sample_dataset)

    def getIntent(self, text):
        parsing = self.nlu_engine.parse(text)

        jsonDump = json.dumps(parsing, indent=2)
        jsonLoads = json.loads(jsonDump)

        return jsonLoads

    def getIntentNameByRecognition(self, jsonLoads):
        return jsonLoads['intent']['intentName']

    def getIntentName(self, text):
        jsonLoad = self.getIntent(text)
        return jsonLoad['intent']['intentName']

        # this code below originally pulled just the intentName - now we return all of the json data so we can use portions as needed
        # inside the other code
        # https://snips-nlu.readthedocs.io/en/latest/tutorial.html
        # Intents Filters
        # In some cases, you may have some extra information regarding the context in which the parsing occurs, and you may already know that some intents won’t be triggered. To leverage that, you can use intents filters and restrict the parsing output to a given list of intents:
        #
        # parsing = engine.parse("Hey, lights on in the lounge !",
        #                         intents=["turnLightOn", "turnLightOff"])
        #
        # jsonDump = json.dumps(parsing, indent=2)
        # jsonLoads = json.loads(jsonDump)
        # intentName = jsonLoads['intent']['intentName']
        #
        # if intentName != "" and intentName != None:
        #     return intentName
        # else:
        #     return "could not find intent"


# snips
    # slots = command['slots']
    # for slot in slots:
    #     name = slot['slotName']
    #     if name == 'cameraNumber':
    #         cameraNumber = int(slot['rawValue'])
    #         print(cameraNumber)
    #         # self.cameras[cameraNumber].addFilter('drawGrid', DrawGrid())
    #         cam = self.cameras[cameraNumber]
    #         print(cam.cameraNumber)
    #         cam.addFilter('drawGrid', DrawGrid())
# elif intentName == 'hideGrid':
    # cameras are in a zero based index so subtract one to get the actual camera number
    # cam.removeFilter('drawGrid')
    # snips
    # slots = command['slots']
    # for slot in slots:
    #     name = slot['slotName']
    #     if name == 'cameraNumber':
    #         cameraNumber = int(slot['rawValue'])
    #         print(cameraNumber)
    #         cam = self.cameras[cameraNumber]
    #         print(cam.cameraNumber)
    #
    #         cam.removeFilter('drawGrid')