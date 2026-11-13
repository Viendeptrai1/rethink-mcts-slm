import sys

def get_word_cores(text):
    import re
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    return [word.lower() for word in words]

def generate_transformations(word):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    transformations = set()
    
    # Delete a single character
    for i in range(len(word)):
        transformations.add(word[:i] + word[i+1:])
    
    # Insert a single alphabetic character
    for i in range(len(word) + 1):
        for char in alphabet:
            transformations.add(word[:i] + char + word[i:])
    
    # Replace a single character by a different alphabetic character
    for i in range(len(word)):
        for char in alphabet:
            if char != word[i]:
                transformations.add(word[:i] + char + word[i+1:])
    
    # Transpose (exchange) any two adjacent characters
    for i in range(len(word) - 1):
        transformed_word = word[:i] + word[i+1] + word[i] + word[i+2:]
        transformations.add(transformed_word)
    
    return transformations

def find_similarly_spelled_words(input_text):
    word_cores = get_word_cores(input_text)
    core_to_similars = {}
    
    for core in word_cores:
        for transformation in generate_transformations(core):
            if transformation in word_cores and transformation != core:
                if core not in core_to_similars:
                    core_to_similars[core] = set()
                core_to_similars[core].add(transformation)
    
    for core in sorted(core_to_similars.keys()):
        similars = sorted(list(core_to_similars[core]))
        print(f"{core}: {' '.join(similars)}")

if __name__ == "__main__":
    input_text = ""
    for line in sys.stdin:
        if line.strip() == "***":
            break
        input_text += line
    
    find_similarly_spelled_words(input_text)