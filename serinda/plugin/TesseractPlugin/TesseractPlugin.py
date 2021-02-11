
class TesseractPlugin:
    def processIntent(self, intent):
        if intent == 'showTesseract' or intent == 'hideTesseract':
            print("inside tesseract plugin")

        return ["", ""]