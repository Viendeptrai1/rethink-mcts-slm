def decrypt(s):
    n = len(s)
    i = 0
    decrypted = []
    while i < n:
        char = s[i]
        count = 0
        while i < n and s[i] == char:
            count += 1
            i += 1
        decrypted.append(char * (count // (len(decrypted) + 1)))
    return ''.join(decrypted)

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    t = data[1]
    result = decrypt(t)
    print(result)