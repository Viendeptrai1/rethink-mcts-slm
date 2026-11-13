def encrypt(s):
    result = []
    for char in s:
        if char.isalpha():
            shift = (2 * 2) % 26
            if char.islower():
                result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
            else:
                result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
        else:
            result.append(char)
    return ''.join(result)