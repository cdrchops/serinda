from textblob import TextBlob

def translateTextBlob(word, language):
    blob = TextBlob(word)  # TextBlob(u'तुम्हारा नाम क्या है')


    text = blob.translate(to=language)

    return str(text)


def translatePhrase(cherokee, phrase):
    print(cherokee + "  " + translateTextBlob(phrase, "es") + "  " + translateTextBlob(phrase, "ja") + "  " + translateTextBlob(phrase, "ru") + "  " + translateTextBlob(phrase, "ar"))


translatePhrase("ᎭᏢ", "where")
translatePhrase("ᎦᏙ", "what")
translatePhrase("ᎯᎳᏴᎢ", "when")
translatePhrase("ᎯᎳ", "how")
translatePhrase("ᎦᏙᎲ", "why")
translatePhrase("ᎦᎪ", "who?")
translatePhrase("ᏙᎯᏧ?", "How are you?")
translatePhrase("ᎣᏍᏓ", "well")
translatePhrase("ᎣᏍᏓᏛ", "very well")
translatePhrase("ᎰᏩ", "no problem")
translatePhrase("ᏂᎯᎾ?", "and you?")
translatePhrase("ᏩᏙ", "thank you")
translatePhrase("ᏩᏙᏛ", "thank you very much")
translatePhrase("ᏗᎪᏪᎵ", "book")
translatePhrase("ᏥᎪᎵᏰᎠ", " I am reading")
translatePhrase("ᏥᎪᏩᏘᎭ", "I see it")
translatePhrase("ᎦᏙ ᎯᎠ?", "What's this?")
translatePhrase("ᎠᏆᏅᏔ", "I know")
