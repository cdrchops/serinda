import os

class ApplicationConstants:
    # this next line is in case we need to go from the root of the drive to this folder... I don't think it's needed
    #   so it's commented out for now
    # basePath = os.path.join("serinda", "serindaMain")
    serindaCommandsYmlFile = os.path.join("intents", "serindaCommands.yml")
    serindaCommandsJSGFFile = os.path.join("intents", "serindaCommands.jsgf")
    pluginPath = os.path.join("serinda", "plugin")
    serindaCommandsJsonFile = os.path.join("intents","serindaCommands.json")
    serindaCommands2JsonFile = os.path.join("intents", "serindaCommands.json")

