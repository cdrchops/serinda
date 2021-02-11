from serinda.plugin.CommandsPlugin.CommandsPlugin import CommandsPlugin
from serinda.plugin.CurrencyConverterPlugin.CurrencyConverterPlugin import CurrencyConverterPlugin
from serinda.plugin.TesseractPlugin.TesseractPlugin import TesseractPlugin
from serinda.plugin.TestPlugin.TestPlugin import TestPlugin
from serinda.plugin.TranslationPlugin.TranslationPlugin import TranslationPlugin
from serinda.plugin.PdfPlugin.PdfPlugin import PdfPlugin


# Processes all plugins
# All new plugins have to be added here to be processed
class PluginManager:
    # new plugins are added here as instances
    # todo: make this readable from a file
    pluginList = [CurrencyConverterPlugin(),
                  TranslationPlugin(),
                  TestPlugin(),
                  PdfPlugin(),
                  TesseractPlugin(),
                  CommandsPlugin()]

    # set the initial text and language values for returning
    # iterate over all of the plugins in the list and call the processIntent
    # if the text is empty then the plugin just processed didn't process the value
    # if the text is not empty then the plugin just processed did process the value and we can return now
    def processPlugins(self, intent):
        [language, text] = ["", ""]
        for i in self.pluginList:
            [language, text] = i.processIntent(intent)

            if text != "":
                break

        return [language, text]
