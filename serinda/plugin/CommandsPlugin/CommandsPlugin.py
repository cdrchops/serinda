
class CommandsPlugin:
    def processIntent(self, intent):
        if intent == 'showCommands' or intent == 'hideCommands':
            print("inside command plugin")

        return ["", ""]