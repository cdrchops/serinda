# https://medium.com/towards-artificial-intelligence/creating-a-voice-recognition-application-with-python-57d8c3e55256
# install pyaudio on windows using wheel directly - make sure you download the version for your matching python3 version
# -- https://stackoverflow.com/questions/52283840/i-cant-install-pyaudio-on-windows-how-to-solve-error-microsoft-visual-c-14
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

# pocketsphinx whl -- https://www.lfd.uci.edu/~gohlke/pythonlibs/

import speech_recognition as sr

class SpeechRec:
    #https://techwithtim.net/tutorials/voice-assistant/wake-keyword/
    def record(self, lang='en'):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            #this records for up to 5 seconds -I'd rather have listen to pay attention to whether or not the user is talking
            #data = r.record(source, duration=5)
            audio = r.listen(source)
            said = ""

            try:
                #can I detect the language?
                if (lang == 'en') :
                    #recognize_sphinx
                    said = r.recognize_google(audio, language='en-US')
                elif (lang == 'es') :
                    #recognize_sphinx
                    said = r.recognize_google(audio, language="es")

            except Exception as e:
                if (str(e) != ""):
                    print("Exception: " + str(e))

        return said.lower()




