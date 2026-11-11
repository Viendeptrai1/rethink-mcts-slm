import sys

def decrypt(t):
    n = len(t)
    s = []
    i = 0
    for j in range(1, 11):
        if i + j > n:
            break
        if t[i:i+j] == t[i] * j:
            s.append(t[i])
            i += j
        else:
            break
    return ''.join(s)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    t = data[1]
    print(decrypt(t))

if __name__ == "__main__":
    main()