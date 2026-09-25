import sys
from collections import defaultdict

def solve(s, m, b):
    n = len(s)
    s = list(s)
    s.sort()
    
    t = []
    b_index = 0
    
    while b_index < m:
        for i in range(n):
            if s[i] == chr(ord('a') + b_index):
                t.append(s[i])
                s.pop(i)
                break
        
        b_index += 1
    
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
        
        result = solve(s, m, b)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()