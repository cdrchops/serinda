from textblob import TextBlob
from googletrans import Translator

#googletrans doesn't always work - using TextBlob for now
class TranslationMatrix:
    #google translate
    def translate(self, word, language='es'):
        translator = Translator()

        #todo later uncomment this so we can detect the language
        #later on we can still detect the language if we want to - otherwise we've explicitly told it what we're going to translate to
        # if translator.detect(word).lang != 'en':
        #     result = ["en", translator.translate(word, dest='en').text]
        # else:
        #     result = ["es", translator.translate(word, dest='es').text]

        # result = [language, translator.translate(word, dest=language).text]
        resultext = translator.translate(text=word, dest=language)


        result = resultext.text

        return result

    #this portion is supposedly deprecated so need to use google translate above
    #todo - find a translation dictionary offline - NN train?
    #todo - also work on Cherokee NN - maybe train through database to find verbs and conjugate them and create rules?
    def translateTextBlob(self, word, language):
        blob = TextBlob(word)  # TextBlob(u'तुम्हारा नाम क्या है')

        # if blob.detect_language() != 'en':
        #     result = ["en", blob.translate(to='en')]
        # else:
        #     result = ["es", blob.translate(to='es')]

        text = blob.translate(to=language)

        return str(text)