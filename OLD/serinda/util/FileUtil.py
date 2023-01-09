#https://stackoverflow.com/questions/3140010/converting-from-utf-16-to-utf-8-in-python-3
# when snips runs it writes out the file on windows as utf-16 - it's possible linux is utf-32
# this will read the intent file in utf-16 and write it out as utf-8
with open("./intents/serindaCommands2.json", 'w', encoding='utf-8') as out_file:
    # read every line. We give open() the encoding so it will return a Unicode string.
    for line in open("./intents/serindaCommands.json", encoding='utf-16'):
        #Replace the characters we want. When you define a string in python it also is automatically a unicode string.
        # No worries about encoding there. Because we opened the file with the utf-8 encoding,
        # the print statement will encode the whole string to utf-8.
        # print(line, out_file)
        out_file.write(line)