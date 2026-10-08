import sys
from collections import defaultdict

def f(x):
    result = 0
    while x > 0:
        if x % 2 == 1:
            result += 1
        x //= 2
    return result

def count_pairs(n, a):
    count_map = defaultdict(int)
    for num in a:
        count_map[f(num)] += 1
    
    total_pairs = 0
    for count in count_map.values():
        if count > 1:
            total_pairs += count * (count - 1) // 2
    
    return total_pairs

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