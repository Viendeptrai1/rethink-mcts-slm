import sys
from collections import defaultdict

def normalize(word):
    return ''.join(c.lower() for c in word if c.isalpha())

def generate_similar_words(word):
    similar_words = set()
    
    # Insertion
    for i in range(len(word) + 1):
        for c in 'abcdefghijklmnopqrstuvwxyz':
            similar_words.add(word[:i] + c + word[i:])
    
    # Deletion
    for i in range(len(word)):
        similar_words.add(word[:i] + word[i+1:])
    
    # Replacement
    for i in range(len(word)):
        for c in 'abcdefghijklmnopqrstuvwxyz':
            if c != word[i]:
                similar_words.add(word[:i] + c + word[i+1:])
    
    # Transposition
    for i in range(len(word) - 1):
        similar_words.add(word[:i] + word[i+1] + word[i] + word[i+2:])
    
    return similar_words

def main():
    input_text = []
    for line in sys.stdin:
        if line.strip() == "***":
            break
        input_text.append(line)
    
    words = []
    for line in input_text:
        words.extend(normalize(word) for word in line.split())
    
    word_to_similar = defaultdict(set)
    
    for word in words:
        similar_words = generate_similar_words(word)
        for similar_word in similar_words:
            if similar_word != word:
                word_to_similar[word].add(similar_word)
                word_to_similar[similar_word].add(word)
    
    result = {}
    for word, similars in word_to_similar.items():
        if len(similars) > 1:
            result[word] = sorted(similars - {word})
    
    if not result:
        print("***")
    else:
        for word in sorted(result.keys()):
            print(f"{word}: {' '.join(result[word])}")

if __name__ == "__main__":
    main()