from serinda.STT.SpeechRec import SpeechRec
from serinda.translations.TranslationMatrix import TranslationMatrix


class TranslationPlugin:
    # def __init__(self):
    #     print('do nothing')

    def processIntent(self, intent):
        language = "en"
        translate = False
        text = ""

        if intent == 'translateToSpanish':
            text = SpeechRec().record('en')
            language = "es"
            translate = True
        elif intent == 'translateToEnglish':
            text = SpeechRec().record('es')
            language = "en"
            translate = True

        if translate:
            # todo: later when we are detecting the language we'll return the language and translated value - for now this isn't needed
            # [language, translatedValue] = TranslationMatrix().translate(text, language)
            # language = language
            # text = translatedValue
            # sayIt = SayIt()
            # if language == 'en':
            #     sayIt.setLang('en')
            # elif language == 'es':
            #     sayIt.setLang('es')

            # print(text)

            #for calling google
            # text = TranslationMatrix().translate(text, language)

            #for textblob
            text = TranslationMatrix().translateTextBlob(text, language)
            # print(text)
            # runtimeerror 'run loop already started'
            # sayIt.sayIt(text)

            # print(language)

        return [language, text]