import sys

def decrypt(t):
    n = len(t)
    for m in range(1, 11):
        s = []
        index = 0
        valid = True
        for i in range(1, m + 1):
            if index + i > n:
                valid = False
                break
            segment = t[index:index + i]
            if len(set(segment)) != 1:
                valid = False
                break
            s.append(segment[0])
            index += i
        if valid and index == n:
            return ''.join(s)
    return ""

if __name__ == "__main__":
    n = int(sys.stdin.readline().strip())
    t = sys.stdin.readline().strip()
    result = decrypt(t)
    print(result)