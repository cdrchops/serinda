# rewritten example from
# https://stackoverflow.com/questions/39064089/python-pyttsx-how-to-use-external-loop/39069269#39069269
import pyttsx3
from sys import platform
import queue
from threading import Thread

class SayIt:
    q = queue.Queue()
    engine = pyttsx3.init()

    def __init__(self):
        if platform == "linux" or platform == "linux2":
            print("nothing here yet")
        elif platform == "darwin":
            # engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Alex')  # en_US
            self.engine.setProperty('voice', 'com.apple.speech.synthesis.voice.karen')  # en_AU
            # engine.setProperty('voice', 'com.apple.speech.synthesis.voice.paulina')#es_mx
            # engine.setProperty('voice', 'com.apple.speech.synthesis.voice.monica')#es_es
        elif platform == "win32":
            # HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0
            # engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
            # HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0
            # engine.setProperty('voice', voices[1].id)  # changing index, changes voices. 1 for female
            # changing index, changes voices. 1 for female
            # self.engine.setProperty('voice',
            #                         'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
            self.engine.setProperty('voice',
                                    'HKEY_LOCAL_MACHINE/SOFTWARE/Microsoft/Speech/Voices/Tokens/TTS_MS_EN-US_ZIRA_11.0')

    def say_loop(self):
        while True:
            self.engine.say(self.q.get())
            self.engine.runAndWait()
            self.q.task_done()

    def sayIt(self, text, language='en'):
        # self.setLang(language)
        self.q.put(text)

    def join(self):
        self.q.join()

    def setLang(self, language):
        if language == 'en':
            self.engine.setProperty('voice', 'com.apple.speech.synthesis.voice.karen')  # en_AU
        elif language == 'es':
            self.engine.setProperty('voice', 'com.apple.speech.synthesis.voice.paulina')
