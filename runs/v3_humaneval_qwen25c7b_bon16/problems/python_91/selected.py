def is_bored(S):
    import re
    sentences = re.split(r'[.?!]\s*', S)
    return sum(sentence.startswith('I') for sentence in sentences)