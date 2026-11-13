def encrypt(s):
    result = []
    for char in s:
        if char.isalpha():
            base = ord('a') if char.islower() else ord('A')
            shifted = (ord(char) - base + 4) % 26
            result.append(chr(base + shifted))
        else:
            result.append(char)
    return ''.join(result)