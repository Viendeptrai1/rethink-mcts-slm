import sys
from collections import defaultdict

def normalize(word):
    return ''.join(c.lower() for c in word if c.isalpha())

def is_similar(word1, word2):
    if len(word1) == len(word2):
        # Check for replace or transpose
        diff_count = sum(c1 != c2 for c1, c2 in zip(word1, word2))
        if diff_count == 1:
            return True
        # Check for transpose
        for i in range(len(word1) - 1):
            if word1[i] == word2[i + 1] and word1[i + 1] == word2[i]:
                return True
    elif len(word1) == len(word2) + 1:
        # Check for delete
        for i in range(len(word1)):
            if word1[:i] + word1[i+1:] == word2:
                return True
    elif len(word1) + 1 == len(word2):
        # Check for insert
        for i in range(len(word2)):
            if word1 == word2[:i] + word2[i+1:]:
                return True
    return False

def find_similar_words(text):
    words = []
    for line in text.splitlines():
        words.extend(normalize(word) for word in line.split())
    
    similar_words = defaultdict(set)
    word_set = set(words)
    
    for word in word_set:
        for candidate in word_set:
            if word != candidate and is_similar(word, candidate):
                similar_words[word].add(candidate)
                similar_words[candidate].add(word)
    
    result = []
    for word in sorted(similar_words.keys()):
        if similar_words[word]:
            result.append(f"{word}: {' '.join(sorted(similar_words[word]))}")
    
    return result if result else ["***"]

if __name__ == "__main__":
    input_text = sys.stdin.read()
    output = find_similar_words(input_text)
    for line in output:
        print(line)