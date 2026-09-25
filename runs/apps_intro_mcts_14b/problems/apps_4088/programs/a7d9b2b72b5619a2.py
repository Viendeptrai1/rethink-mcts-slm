import sys
from collections import deque

def calculate_b(t):
    m = len(t)
    b = [0] * m
    for i in range(m):
        for j in range(m):
            if t[j] > t[i]:
                b[i] += abs(i - j)
    return b

def find_t(s, m, b):
    s = sorted(s)
    t = [''] * m
    used = [False] * len(s)
    
    def backtrack(pos):
        if pos == m:
            return True
        for i in range(len(s)):
            if not used[i]:
                t[pos] = s[i]
                used[i] = True
                if calculate_b(t[:pos+1]) == b[:pos+1]:
                    if backtrack(pos + 1):
                        return True
                used[i] = False
        return False
    
    backtrack(0)
    return ''.join(t)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    q = int(data[index])
    index += 1
    results = []
    
    for _ in range(q):
        s = data[index]
        index += 1
        m = int(data[index])
        index += 1
        b = list(map(int, data[index:index + m]))
        index += m
        
        t = find_t(s, m, b)
        results.append(t)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()