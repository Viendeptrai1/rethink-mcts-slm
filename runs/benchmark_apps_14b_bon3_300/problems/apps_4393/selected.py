import sys

def decrypt(t):
    s = []
    i = 0
    count = 1
    while i < len(t):
        s.append(t[i])
        i += count
        count += 1
    return ''.join(s)

if __name__ == "__main__":
    n = int(sys.stdin.readline().strip())
    t = sys.stdin.readline().strip()
    result = decrypt(t)
    print(result)