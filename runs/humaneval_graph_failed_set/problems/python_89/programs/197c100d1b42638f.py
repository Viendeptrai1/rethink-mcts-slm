def encrypt(s):
    # Define the alphabet
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    encrypted_string = []
    
    # Iterate over each character in the input string
    for char in s:
        # Find the index of the character in the alphabet
        original_index = alphabet.find(char)
        # Check if the character is found in the alphabet
        if original_index != -1:
            # Calculate the new index after shifting by 4 positions
            new_index = (original_index + 4) % 26
            # Append the new character to the list
            encrypted_string.append(alphabet[new_index])
    
    # Join the list into a string and return
    return ''.join(encrypted_string)