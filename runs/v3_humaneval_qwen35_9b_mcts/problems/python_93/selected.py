def encode(message):
    vowels = set('aeiouAEIOU')
    result = []
    for char in message:
        if not char.isalpha():
            result.append(char)
            continue
        
        # Swap case
        if char.islower():
            swapped = char.upper()
        else:
            swapped = char.lower()
        
        # Check if the swapped character is a vowel and shift it
        if swapped in vowels:
            # Determine the base offset for the vowel
            if swapped in 'AEIOU':
                base = ord('A')
            else:
                base = ord('a')
            
            # Calculate the new character position
            offset = ord(swapped) - base
            new_offset = (offset + 2) % 26
            new_char = chr(base + new_offset)
            result.append(new_char)
        else:
            result.append(swapped)
    
    return ''.join(result)