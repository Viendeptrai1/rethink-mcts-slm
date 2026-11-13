def decrypt_repeating_cipher(n, t):
    decrypted = []
    i = 0
    while i < n:
        current_char = t[i]
        count = 1
        while i + 1 < n and t[i + 1] == current_char:
            count += 1
            i += 1
        decrypted.append(current_char)
        i += 1
    return ''.join(decrypted)

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    t = data[1]
    result = decrypt_repeating_cipher(n, t)
    print(result)