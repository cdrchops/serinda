# originally from https://www.geeksforgeeks.org/python-append-content-of-one-text-file-to-another/ - edited to my needs
# loop through plugins directory pulling all commands.yml files
# merge all of those files together into one
# then run the following command to generate the commands json file
from pathlib import Path

from serinda.constants.ApplicationConstants import ApplicationConstants

class MergeCommandFiles:
     # before anything can begin we clean the serinda commands yml and json files so they don't contain any previous configurations
     def __init__(self):
          f2 = open(ApplicationConstants.serindaCommandsYmlFile, "w")
          f2.write("")
          f2.close()
          json = open(ApplicationConstants.serindaCommandsJsonFile, "w")
          json.write("")
          json.close()

     # make the combined yml file empty then append every command file from the specified directory
     def mergeFiles(self):
          pathlist = Path(ApplicationConstants.pluginPath).glob('**/commands.yml')

          for path in pathlist:
               firstfile = str(path)
               # opening first file in append mode and second file in read mode
               f1 = open(firstfile, 'r')
               f2 = open(ApplicationConstants.serindaCommandsYmlFile, 'a+')

               # appending the contents of the second file to the first file
               f2.write(f1.read())
               f2.write("\n")

               # closing the files
               f1.close()
               f2.close()