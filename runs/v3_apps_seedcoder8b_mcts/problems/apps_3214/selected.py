import sys
from collections import defaultdict

def get_word_cores(text):
    words = text.split()
    cores = []
    for word in words:
        core = ''.join(filter(str.isalpha, word)).lower()
        if core:
            cores.append(core)
    return cores

def generate_variants(word):
    variants = set()
    length = len(word)
    
    # Deletion
    for i in range(length):
        variants.add(word[:i] + word[i+1:])
    
    # Insertion
    for i in range(length + 1):
        for c in 'abcdefghijklmnopqrstuvwxyz':
            variants.add(word[:i] + c + word[i:])
    
    # Replacement
    for i in range(length):
        for c in 'abcdefghijklmnopqrstuvwxyz':
            if word[i] != c:
                variants.add(word[:i] + c + word[i+1:])
    
    # Transposition
    for i in range(length - 1):
        variants.add(word[:i] + word[i+1] + word[i] + word[i+2:])
    
    return variants

def find_similar_words(cores):
    similar_words = defaultdict(set)
    for core in cores:
        variants = generate_variants(core)
        for variant in variants:
            if variant in cores and variant != core:
                similar_words[core].add(variant)
                similar_words[variant].add(core)
    
    result = []
    for core in sorted(similar_words.keys()):
        similar = sorted(similar_words[core])
        if similar:
            result.append(f"{core}: {' '.join(similar)}")
    
    return result

def main():
    input_lines = sys.stdin.read().strip().split('\n')
    if input_lines[-1] != "***":
        return
    
    input_lines = input_lines[:-1]
    text = ' '.join(input_lines)
    cores = get_word_cores(text)
    similar_word_list = find_similar_words(cores)
    
    if similar_word_list:
        for line in similar_word_list:
            print(line)
    else:
        print("***")

if __name__ == "__main__":
    main()