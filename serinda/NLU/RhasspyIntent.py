# https://pypi.org/project/rhasspy-nlu/

import rhasspynlu
import io

class RhasspyIntent:
    intentFile = None
    intents = None
    graph = None

    def __init__(self, rhasspyConfig="./intents/serindaCommands.ini"):
        f = open(rhasspyConfig, "r")
        self.intentFile = f.read()
        # Load and parse
        self.intents = rhasspynlu.parse_ini(self.intentFile)

        self.graph = rhasspynlu.intents_to_graph(self.intents)

    def getIntent(self, text):

        # recognitions = rhasspynlu.recognize("set brightness to two", graph)
        # assert recognitions[0].tokens[-1] == 2
        #
        # recognitions = rhasspynlu.recognize("set brightness to one", graph)
        # assert recognitions[0].tokens[-1] == 1

        recognitions = rhasspynlu.recognize(text, self.graph)
        return recognitions

    def getIntentNameByRecognition(self, recognitions):
        return recognitions[0].intent.name


    def getIntentName(self, text):
        recognitions = self.getIntent(text)
        return recognitions[0].intent.name
