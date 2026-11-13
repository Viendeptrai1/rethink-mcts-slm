def encode(message):
    vowels = 'aeiou'
    result = []
    
    for char in message:
        if char.isalpha():
            # Swap case
            if char.islower():
                swapped = char.upper()
            else:
                swapped = char.lower()
            
            # Check if the original character was a vowel
            original_lower = char.lower()
            if original_lower in vowels:
                # Find position in alphabet
                index = ord(original_lower) - ord('a')
                new_index = (index + 2) % 26
                new_char = chr(new_index + ord('a'))
                # Apply the swapped case to the new character
                if char.islower():
                    new_char = new_char.upper()
                else:
                    new_char = new_char.lower()
                swapped = new_char
            
            result.append(swapped)
        else:
            # Keep non-letter characters as is
            result.append(char)
    
    return ''.join(result)