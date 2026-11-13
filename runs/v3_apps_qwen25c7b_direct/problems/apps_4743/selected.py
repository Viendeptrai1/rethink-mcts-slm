def translate_to_nimionese(sentence):
    # Define the mapping for the first letter of the word
    first_letter_map = {
        'a': 'b', 'b': 'c', 'c': 'd', 'd': 'g', 'e': 'k', 'f': 'n',
        'g': 'p', 'h': 't', 'i': 'b', 'j': 'c', 'k': 'd', 'l': 'g',
        'm': 'k', 'n': 'p', 'o': 't', 'p': 'b', 'q': 'c', 'r': 'd',
        's': 'g', 't': 'p', 'u': 't', 'v': 'b', 'w': 'c', 'x': 'd',
        'y': 'g', 'z': 'k'
    }
    
    # Define the mapping for "each" to "Dach"
    each_to_dach = {'each': 'Dach'}
    
    # Define the mapping for hard consonants in subsequent syllables
    subsequent_consonant_map = {
        'b': 'b', 'c': 'c', 'd': 'd', 'g': 'g', 'k': 'k', 'n': 'n',
        'p': 'p', 't': 't'
    }
    
    # Split the sentence into words
    words = sentence.split()
    
    # Translate each word
    translated_words = []
    for word in words:
        # Replace "each" with "Dach"
        if word.lower() == 'each':
            translated_word = each_to_dach[word]
        else:
            # Extract the first letter and map it
            first_letter = word[0].lower()
            new_first_letter = first_letter_map[first_letter]
            
            # Map subsequent hard consonants
            new_word = new_first_letter + ''.join(subsequent_consonant_map.get(c.lower(), c) for c in word[1:])
            
            # Add the appropriate ending
            if new_word[-1] in subsequent_consonant_map:
                last_hard_consonant = new_word[-1]
                if ord(last_hard_consonant) <= ord('d'):
                    new_word += 'ah'
                elif ord(last_hard_consonant) <= ord('g'):
                    new_word += 'oh'
                else:
                    new_word += 'uh'
        
        # Append the translated word to the list
        translated_words.append(new_word)
    
    # Join the translated words back into a sentence
    translated_sentence = ' '.join(translated_words)
    
    return translated_sentence

# Read input from standard input
import sys
input_sentence = sys.stdin.read().strip()

# Translate the sentence to Nimionese
translated_output = translate_to_nimionese(input_sentence)

# Print the translated sentence to standard output
print(translated_output)