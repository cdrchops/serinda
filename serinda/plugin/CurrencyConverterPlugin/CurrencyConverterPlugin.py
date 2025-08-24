from serinda.STT.SpeechRec import SpeechRec

class CurrencyConverterPlugin:
    dopRate = 0.0170969
    usdRate = 58.4900

    # 3,300 = 56.4199 DOP-USD

    def processIntent(self, intent):
        text = ""
        language = ""
        if intent == 'convertToDOP':
            # yield 'data:{}\n\n'.format("lang=en, text=What amount would you like to convert?")
            text = self.convert('d')
        elif intent == 'convertToUSD':
            # yield 'data:{}\n\n'.format("lang=en, text=What amount would you like to convert?")
            text = self.convert()

        return [language, text]

    # converting to USD you divide; converting to DOP you multiply
    def convert(self, multdiv='m'):
        amount = SpeechRec().record()
        if amount != "":
            tmpamt = round(float(amount), 2)
            if multdiv == 'd':
                tmpflt = round(tmpamt / self.usdRate, 2)
            else:
                tmpflt = round(tmpamt * self.usdRate, 2)

            return str(tmpflt)
        else:
            return "amount was invalid"
