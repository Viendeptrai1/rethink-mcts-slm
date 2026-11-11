import sys

def translate_to_nimionese(sentence):
    def nearest_hard_consonant(c):
        hard_consonants = 'bcdfgknpt'
        return min(hard_consonants, key=lambda x: abs(ord(x) - ord(c.lower())))

    def translate_word(word):
        if word.lower() == "each":
            return "Dach"
        
        # Replace first letter with nearest hard consonant
        first_letter = nearest_hard_consonant(word[0])
        translated_word = first_letter + word[1:]
        
        # Replace subsequent hard consonants with the first one
        translated_word = ''.join([first_letter if c in 'bcdfgknpt' else c for c in translated_word])
        
        # Add ending sound
        if translated_word[-1] in 'bcdfgknpt':
            translated_word += 'ah'
        else:
            last_hard_consonant_index = max([i for i, c in enumerate(translated_word) if c in 'bcdfgknpt'], default=-1)
            if last_hard_consonant_index != -1:
                translated_word += ['ah', 'oh', 'uh'][min(['a', 'o', 'u'].index(c) for c in translated_word[last_hard_consonant_index+1:])]
            else:
                translated_word += 'ah'
        
        return translated_word

    # Split sentence into words, remove dashes, and translate each word
    words = sentence.replace('-', '').split()
    translated_words = [translate_word(word) for word in words]
    
    # Join translated words back into a sentence
    return ' '.join(translated_words)

# Read input from stdin
input_sentence = sys.stdin.read().strip()

# Translate and print the result
print(translate_to_nimionese(input_sentence))