def decrypt(t):
    s = ""
    i = 0
    while i < len(t):
        char = t[i]
        count = 0
        while i < len(t) and t[i] == char:
            count += 1
            i += 1
        s += char * (count // (len(s) + 1))
    return s

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    t = data[1]
    print(decrypt(t))