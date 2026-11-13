import sys
import re
from collections import defaultdict

def get_core(word):
    return re.sub(r'[^a-z]', '', word.lower())

def is_similar(word1, word2):
    if len(word1) > len(word2):
        word1, word2 = word2, word1
    if len(word2) - len(word1) > 1:
        return False

    i, j, edits = 0, 0, 0
    while i < len(word1) and j < len(word2):
        if word1[i] != word2[j]:
            edits += 1
            if edits > 1:
                return False
            if len(word1) < len(word2):
                i -= 1
            elif len(word1) > len(word2):
                j -= 1
        i += 1
        j += 1
    
    return edits <= 1

def find_similar_words(text):
    words = re.findall(r'\b\w+\b', text)
    cores = [get_core(word) for word in words]
    similar_dict = defaultdict(set)

    for i, core in enumerate(cores):
        for j, other_core in enumerate(cores):
            if i != j and core != other_core and is_similar(core, other_core):
                similar_dict[core].add(other_core)
                similar_dict[other_core].add(core)

    return {k: sorted(v) for k, v in similar_dict.items() if v}

def main():
    input_lines = sys.stdin.read().strip().split('\n')
    if input_lines[-1] != '***':
        return
    input_lines.pop()

    text = ' '.join(input_lines)
    similar_words_dict = find_similar_words(text)

    if not similar_words_dict:
        print('***')
    else:
        for word_core in sorted(similar_words_dict.keys()):
            print(f"{word_core}: {' '.join(similar_words_dict[word_core])}")

if __name__ == "__main__":
    main()