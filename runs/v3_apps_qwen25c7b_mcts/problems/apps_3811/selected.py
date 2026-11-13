import sys

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def find_wcd(pairs):
    min_val = min(min(pair) for pair in pairs)
    for d in range(2, min_val + 1):
        if all(any(x % d == 0 for x in pair) for pair in pairs):
            return d
    return -1

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    pairs = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(n)]
    
    result = find_wcd(pairs)
    print(result)