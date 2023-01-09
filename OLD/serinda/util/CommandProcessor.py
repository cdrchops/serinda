from serinda.NLU.NLUFactory import NLUFactory
from serinda.STT.SpeechRec import SpeechRec
from serinda.plugin.PluginManager import PluginManager


# TODO: separate out processes and return values to the page correctly
# TODO: come up with a return object that can be used on the front end for nearly every response
#          look at the notes/javascriptCode.txt file for ideas
class CommandProcessor:
    nluIntentProcessor = None

    def __init__(self, nluFactoryName):
        self.WAKE = "bob"
        self.pluginManager = PluginManager()
        self.nluIntentProcessor = NLUFactory().getIntentProcessor(nluFactoryName)


    def processCommand(self, request, cameraPool):
        while True:
            text = SpeechRec().record()
            if text.count(self.WAKE) > 0:
                yield 'data:{}\n\n'.format("lang=en, text=I am ready.")
                text = SpeechRec().record()

                intent = self.nluIntentProcessor.getIntent(text)
                intentName = self.nluIntentProcessor.getIntentNameByRecognition(intent)
                # this is where tracking by grid is going to need to be adjusted since we're passing the data to the
                #   command processes

                yield 'data:{}\n\n'.format("lang=en, text=intent is " + intentName)
                language = "en"

                if intentName == '':
                    # sayIt.setLang("en")
                    # sayIt.sayIt("What was that? I didn't hear anything.")
                    yield 'data:{}\n\n'.format("lang=en, text=What was that? I didn't hear anything.")
                else:
                    cameraPool.setCommand(intent, self.nluIntentProcessor)
                    # # if there's something specific you want to interact with your user about this is where you do it
                    # if intentName == 'convertToDOP' or intentName == 'convertToUSD':
                    #     yield 'data:{}\n\n'.format("lang=en, text=What amount would you like to convert?")
                    # elif intentName == 'showGrid' or intentName == 'hideGrid':
                    #     cameraPool.setCommand(intentName)
                    #
                    # [language, text] = self.pluginManager.processPlugins(intentName)

                if language == "":
                    language = "en"

                # hack b/c I couldn't get json to format correctly
                formatItem = "lang=" + language + ", text=" + text

                # sayIt.setLang(language)
                # sayIt.sayIt(text)
                yield 'data:{}\n\n'.format(formatItem)

    def processCommandOriginal(self, cameraPool):
        while True:
            text = SpeechRec().record()

            if text.count(self.WAKE) > 0:
                yield 'data:{}\n\n'.format("lang=en, text=I am ready.")
                text = SpeechRec().record()

                intent = self.nluIntentProcessor.getIntent(text)
                intentName = self.nluIntentProcessor.getIntentNameByRecognition(intent)
                # this is where tracking by grid is going to need to be adjusted since we're passing the data to the command processes

                yield 'data:{}\n\n'.format("lang=en, text=intent is " + intentName)
                language = "en"

                if intentName == '':
                    yield 'data:{}\n\n'.format("lang=en, text=What was that? I didn't hear anything.")
                else:
                    # if there's something specific you want to interact with your user about this is where you do it
                    if intentName == 'convertToDOP' or intentName == 'convertToUSD':
                        yield 'data:{}\n\n'.format("lang=en, text=What amount would you like to convert?")
                    elif intentName == 'showGrid' or intentName == 'hideGrid':
                        cameraPool.setCommand(intentName)

                    [language, text] = self.pluginManager.processPlugins(intentName)

                if language == "":
                    language = "en"

                # hack b/c I couldn't get json to format correctly
                formatItem = "lang=" + language + ", text=" + text
                yield 'data:{}\n\n'.format(formatItem)

    # for now this is just for testing camera plugins
    def processCommand2(self, cameraPool, text):
        intent = self.nluIntentProcessor.getIntent(text)
        cameraPool.setCommand(intent, self.nluIntentProcessor)
