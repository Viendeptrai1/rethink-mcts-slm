import sys
from collections import Counter

def f(x):
    result = 0
    while x > 0:
        result += x & 1
        x >>= 1
    return result

def count_pairs(n, a):
    freq = Counter(f(ai) for ai in a)
    count = 0
    for value in freq.values():
        if value > 1:
            count += value * (value - 1) // 2
    return count

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    result = count_pairs(n, a)
    print(result)

if __name__ == "__main__":
    main()