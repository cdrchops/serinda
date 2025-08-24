# from serinda.NLU.RhasspyIntent import RhasspyIntent
# from serinda.NLU.SnipsIntent import SnipsIntent
from serinda.NLU.JSGFIntent import JSGFIntent
from serinda.NLU.PocketSphinxIntent import PocketSphinxIntent


# Alternatives to Snips and Rhasspy
# https://pocketsphinx.readthedocs.io/en/latest/index.html
# https://github.com/drmfinlay/pyjsgf

class NLUFactory:
    def getIntentProcessor(self, nluFactoryName):
        print("Loading NLU " + nluFactoryName)
        if nluFactoryName == 'rhasspy':
            # return RhasspyIntent()
            return PocketSphinxIntent()
        elif nluFactoryName == 'snips':
            # return SnipsIntent()
            return PocketSphinxIntent()
        elif nluFactoryName == 'sphinx':
            return PocketSphinxIntent()
        elif nluFactoryName == 'jsgf':
            return JSGFIntent()
