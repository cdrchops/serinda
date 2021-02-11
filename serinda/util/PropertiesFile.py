import jprops

class PropertiesFile:
    propsFile = ""
    propsFileName = "./serinda.props"

    def __init__(self):
        self.read()

    def read(self):
        with open(self.propsFileName) as fp:
            self.propsFile = jprops.load_properties(fp)

    def write(self):
        print("does nothing yet but should write the propsFile in memory to a physical props file")

    def get(self, propertyName):
        return self.propsFile.get(propertyName)

    def put(self, propertyName, propertyValue):
        print('does nothing yet, but should write the key and value to the props file')