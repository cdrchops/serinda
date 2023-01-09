from serinda.NLU.RhasspyIntent import RhasspyIntent
from serinda.NLU.SnipsIntent import SnipsIntent


class NLUFactory:
    def getIntentProcessor(self, nluFactoryName):
        if nluFactoryName == 'rhasspy':
            return RhasspyIntent()
        elif nluFactoryName == 'snips':
            return SnipsIntent()
