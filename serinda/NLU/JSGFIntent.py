from jsgf import parse_grammar_string

class JSGFIntent:
    intentFile = None
    intents = None
    graph = None

    def __init__(self, jsgfConfig="./intents/example.jsgf"):
        f = open(jsgfConfig, "r")
        self.intentFile = f.read()
        # Load and parse
        self.intents = parse_grammar_string(self.intentFile)
        #
        # self.graph = rhasspynlu.intents_to_graph(self.intents)

    def getIntent(self, text):
        # The grammar.find_matching_rules() method finds rules that match the text.
        matches = self.intents.find_matching_rules(text)

        if matches:
            # The first match is usually the most relevant.
            matching_rule = matches[0]

            # The rule name is the intent.
            intent_name = matching_rule.name

            print(intent_name)

            # Tags are used to capture specific parts of the speech input.
            # This example uses pyjsgf's tagging feature for demonstration.
            # See Step 4 for an example with tags.
            tags = matching_rule.tags
            return intent_name, tags

        return None, None

        # recognitions = rhasspynlu.recognize("set brightness to two", graph)
        # assert recognitions[0].tokens[-1] == 2
        #
        # recognitions = rhasspynlu.recognize("set brightness to one", graph)
        # assert recognitions[0].tokens[-1] == 1

        # recognitions = rhasspynlu.recognize(text, self.graph)
        # return recognitions
        return None

    def getIntentNameByRecognition(self, matching_rule):
        return matching_rule.name

    def getIntentName(self, text):
        [intent_name, tags] = self.getIntent(text)
        return intent_name