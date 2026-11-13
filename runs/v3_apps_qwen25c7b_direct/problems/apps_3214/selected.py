import sys

def get_word_cores(text):
    import re
    return set(re.findall(r'\b[a-zA-Z]+\b', text.lower()))

def generate_similar(word_core):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    similar_words = set()
    
    # Delete a single character
    for i in range(len(word_core)):
        similar_words.add(word_core[:i] + word_core[i+1:])
    
    # Insert a single alphabetic character
    for i in range(len(word_core) + 1):
        for char in alphabet:
            similar_words.add(word_core[:i] + char + word_core[i:])
    
    # Replace a single character by a different alphabetic character
    for i in range(len(word_core)):
        for char in alphabet:
            if char != word_core[i]:
                similar_words.add(word_core[:i] + char + word_core[i+1:])
    
    # Transpose (exchange) any two adjacent characters
    for i in range(len(word_core) - 1):
        similar_words.add(word_core[:i] + word_core[i+1] + word_core[i] + word_core[i+2:])
    
    return similar_words

def find_similarly_spelled_words():
    word_cores = set()
    similar_pairs = {}
    
    for line in sys.stdin:
        if line.strip() == "***":
            break
        word_cores.update(get_word_cores(line))
    
    for word_core in word_cores:
        similar_words = generate_similar(word_core)
        for similar_word in similar_words:
            if similar_word in word_cores and similar_word != word_core:
                if word_core not in similar_pairs:
                    similar_pairs[word_core] = set()
                if similar_word not in similar_pairs:
                    similar_pairs[similar_word] = set()
                similar_pairs[word_core].add(similar_word)
                similar_pairs[similar_word].add(word_core)
    
    for word_core in sorted(similar_pairs.keys()):
        print(f"{word_core}: {' '.join(sorted(similar_pairs[word_core]))}")

if __name__ == "__main__":
    find_similarly_spelled_words()