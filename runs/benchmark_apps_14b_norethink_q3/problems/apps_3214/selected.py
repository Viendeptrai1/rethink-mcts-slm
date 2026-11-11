import sys
from collections import defaultdict

def normalize_word(word):
    return ''.join(c.lower() for c in word if c.isalpha())

def is_similar(word1, word2):
    if len(word1) == len(word2):
        # Check for replace or transpose
        diff_count = sum(c1 != c2 for c1, c2 in zip(word1, word2))
        if diff_count == 1:
            return True
        # Check for transpose
        for i in range(len(word1) - 1):
            if word1[i] == word2[i+1] and word1[i+1] == word2[i]:
                return True
    elif len(word1) + 1 == len(word2):
        # Check for insert
        for i in range(len(word2)):
            if word1 == word2[:i] + word2[i+1:]:
                return True
    elif len(word1) - 1 == len(word2):
        # Check for delete
        for i in range(len(word1)):
            if word1[:i] + word1[i+1:] == word2:
                return True
    return False

def find_similar_words(text):
    words = []
    for line in text.splitlines():
        words.extend(normalize_word(word) for word in line.split())
    
    word_dict = defaultdict(set)
    for i, word1 in enumerate(words):
        for j, word2 in enumerate(words):
            if i != j and is_similar(word1, word2):
                word_dict[word1].add(word2)
                word_dict[word2].add(word1)
    
    result = {}
    for word, similar_words in word_dict.items():
        if similar_words:
            result[word] = sorted(similar_words - {word})
    
    if not result:
        print("***")
    else:
        for word in sorted(result):
            print(f"{word}: {' '.join(result[word])}")

if __name__ == "__main__":
    text = ""
    for line in sys.stdin:
        if line.strip() == "***":
            break
        text += line
    find_similar_words(text)