def encrypt(s):
    encrypted = []
    for char in s:
        if 'a' <= char <= 'z':
            offset = (ord(char) - ord('a') + 2 * 2) % 26
            encrypted.append(chr(ord('a') + offset))
        elif 'A' <= char <= 'Z':
            offset = (ord(char) - ord('A') + 2 * 2) % 26
            encrypted.append(chr(ord('A') + offset))
        else:
            encrypted.append(char)
    return ''.join(encrypted)