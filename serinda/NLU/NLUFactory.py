# from serinda.NLU.RhasspyIntent import RhasspyIntent
from serinda.NLU.SnipsIntent import SnipsIntent


class NLUFactory:
    def getIntentProcessor(self, nluFactoryName):
        print("Loading NLU " + nluFactoryName)
        if nluFactoryName == 'rhasspy':
            return SnipsIntent()
            # return RhasspyIntent()
        elif nluFactoryName == 'snips':
            return SnipsIntent()
