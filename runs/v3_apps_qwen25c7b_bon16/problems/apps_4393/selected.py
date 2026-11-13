def decrypt(t):
    s = ''
    i = 0
    while i < len(t):
        j = i + 1
        while j < len(t) and t[j] == t[i]:
            j += 1
        count = j - i
        s += t[i]
        i = j
    return s

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    t = data[1]
    result = decrypt(t)
    print(result)