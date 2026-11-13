from collections import Counter

def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    def f(x):
        if x == 0:
            return 0
        elif x % 2 == 0:
            return f(x // 2)
        else:
            return f(x // 2) + 1
    
    freq = Counter(f(ai) for ai in a)
    
    result = 0
    for count in freq.values():
        result += count * (count - 1) // 2
    
    print(result)

solve()