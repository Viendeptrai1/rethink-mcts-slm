import sys

def generate_transformations(word):
    transformations = set()
    n = len(word)
    
    # Delete a single character
    for i in range(n):
        transformations.add(word[:i] + word[i+1:])
    
    # Insert a single alphabetic character
    for i in range(n + 1):
        for char in 'abcdefghijklmnopqrstuvwxyz':
            transformations.add(word[:i] + char + word[i:])
    
    # Replace a single character by a different alphabetic character
    for i in range(n):
        for char in 'abcdefghijklmnopqrstuvwxyz':
            if char != word[i]:
                transformations.add(word[:i] + char + word[i+1:])
    
    # Transpose (exchange) any two adjacent characters
    for i in range(n - 1):
        transformations.add(word[:i] + word[i+1] + word[i] + word[i+2:])
    
    return transformations

def find_similar_words(text):
    words = []
    current_word = ''
    for char in text:
        if char.isalpha():
            current_word += char.lower()
        elif current_word:
            words.append(current_word)
            current_word = ''
    if current_word:
        words.append(current_word)
    
    similar_words_dict = {}
    for word in words:
        transformations = generate_transformations(word)
        for transformed_word in transformations:
            if transformed_word in words and transformed_word != word:
                if word not in similar_words_dict:
                    similar_words_dict[word] = set()
                similar_words_dict[word].add(transformed_word)
    
    sorted_keys = sorted(similar_words_dict.keys())
    result = []
    for key in sorted_keys:
        result.append(f"{key}: {' '.join(sorted(similar_words_dict[key]))}")
    
    return result

if __name__ == "__main__":
    text = ""
    for line in sys.stdin:
        if line.strip() == "***":
            break
        text += line
    
    result = find_similar_words(text)
    if result:
        for line in result:
            print(line)
    else:
        print("***")