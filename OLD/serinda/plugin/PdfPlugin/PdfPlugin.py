
class PdfPlugin:
    def processIntent(self, intent):
        if intent == 'showPDF' or intent == 'hidePDF':
            print("inside pdf plugin")

        return ["", ""]