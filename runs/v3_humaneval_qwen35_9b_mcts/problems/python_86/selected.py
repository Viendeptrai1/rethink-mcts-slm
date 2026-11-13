import re

def anti_shuffle(s):
    def sort_word(match):
        word = match.group(0)
        return ''.join(sorted(word))
    
    return re.sub(r'\S+', sort_word, s)