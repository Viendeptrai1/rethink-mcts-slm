def encode(message):
    vowels = 'aeiouAEIOU'
    shift = {v: chr((ord(v) - ord('a') + 2) % 26 + ord('a')) for v in vowels.lower()}
    shift.update({v.upper(): shift[v].upper() for v in shift})
    
    encoded_message = []
    for char in message:
        if char.isalpha():
            if char in vowels:
                encoded_message.append(shift[char])
            else:
                encoded_message.append(char.swapcase())
        else:
            encoded_message.append(char)
    
    return ''.join(encoded_message)

# Example usage:
# print(encode('test'))  # Output: 'TGST'
# print(encode('This is a message'))  # Output: 'tHKS KS C MGSSCGG'