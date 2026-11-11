import sys

def decrypt(t):
    s = []
    i = 0
    for j in range(1, len(t) + 1):
        if t[i:i+j] == t[i] * j:
            s.append(t[i])
            i += j
        else:
            return ""
    return "".join(s)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    t = data[1]
    result = decrypt(t)
    print(result)

if __name__ == "__main__":
    main()