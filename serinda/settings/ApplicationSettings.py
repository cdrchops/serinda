
class ApplicationSettings:


    def __init__(self):
        print("Application settings initialized")

    def pyttsxSynthesizer(self):
        global pyttsx_synthesizer
        return pyttsx_synthesizer



    # TODO: set up in startup
    # put in the settings

    # sapi5 - SAPI5 on Windows
    # nsss - NSSpeechSynthesizer on Mac OS X
    # espeak - eSpeak on every other platform
