def encode(message):
    vowels = 'aeiouAEIOU'
    result = []
    
    for char in message:
        if char.isalpha():
            # Swap case
            swapped = char.swapcase()
            
            # Check if the original character was a vowel
            if char.lower() in 'aeiou':
                # Replace with letter 2 places ahead
                # We need to shift the original vowel, not the swapped one
                base = ord('a') if char.islower() else ord('A')
                offset = ord(char) - base
                new_offset = (offset + 2) % 26
                new_char = chr(base + new_offset)
                # Apply the swapped case to the new character
                if char.islower():
                    new_char = new_char.upper()
                else:
                    new_char = new_char.lower()
                result.append(new_char)
            else:
                result.append(swapped)
        else:
            # Non-letter characters remain unchanged (though problem says assume only letters)
            result.append(char)
    
    return ''.join(result)