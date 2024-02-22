import nltk
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

sentence = "Whether or not"

# Tokenize: Split the sentence into words
word_list = nltk.word_tokenize(sentence)
print(word_list)

# Lemmatize list of words and join
lemmatized_output = ' '.join([lemmatizer.lemmatize(w) for w in word_list])
print(lemmatized_output)
