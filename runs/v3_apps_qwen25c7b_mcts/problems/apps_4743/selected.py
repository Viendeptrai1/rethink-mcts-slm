def translate_to_nimionese(sentence):
    import re
    
    # Define the mapping for initial consonants
    initial_consonant_map = {
        'B': 'G', 'C': 'G', 'D': 'G', 'F': 'G', 'G': 'G',
        'H': 'J', 'K': 'L', 'L': 'M', 'M': 'N', 'N': 'N',
        'P': 'Q', 'R': 'S', 'S': 'T', 'T': 'T', 'V': 'W',
        'W': 'X', 'X': 'Y', 'Y': 'Z', 'Z': 'Z'
    }
    
    # Define the mapping for subsequent consonants
    subsequent_consonant_map = {
        'B': 'B', 'C': 'C', 'D': 'D', 'F': 'F', 'G': 'G',
        'H': 'H', 'K': 'K', 'L': 'L', 'M': 'M', 'N': 'N',
        'P': 'P', 'R': 'R', 'S': 'S', 'T': 'T', 'V': 'V',
        'W': 'W', 'X': 'X', 'Y': 'Y', 'Z': 'Z'
    }
    
    # Define the mapping for "each"
    each_word = "Dach"
    
    # Split the sentence into words
    words = sentence.split()
    
    # Process each word
    translated_words = []
    for word in words:
        # Replace "each" with "Dach"
        if word == "each":
            translated_words.append(each_word)
            continue
        
        # Extract the initial consonant and the rest of the word
        initial_consonant = word[0].upper()
        rest_of_word = word[1:]
        
        # Translate the initial consonant
        new_initial_consonant = initial_consonant_map.get(initial_consonant, initial_consonant)
        
        # Translate the rest of the word
        new_rest_of_word = ''
        for char in rest_of_word:
            if char.upper() in subsequent_consonant_map:
                new_rest_of_word += subsequent_consonant_map[char.upper()].lower()
            else:
                new_rest_of_word += char.lower()
        
        # Add the appropriate ending sound
        if new_rest_of_word[-1] in subsequent_consonant_map:
            last_consonant = new_rest_of_word[-1].upper()
            ending_sound = subsequent_consonant_map[last_consonant].lower() + 'a' * (last_consonant.isupper())
        else:
            ending_sound = 'a'
        
        # Combine the parts and add to the list
        translated_word = new_initial_consonant + new_rest_of_word + ending_sound
        translated_words.append(translated_word)
    
    # Join the translated words back into a sentence
    translated_sentence = ' '.join(translated_words)
    
    return translated_sentence

# Example usage
if __name__ == "__main__":
    import sys
    input_sentence = sys.stdin.read().strip()
    result = translate_to_nimionese(input_sentence)
    print(result)