import re

def is_bored(S):
    sentences = re.split(r'[.?!]\s*', S)
    return sum(sentence.startswith('I') for sentence in sentences)