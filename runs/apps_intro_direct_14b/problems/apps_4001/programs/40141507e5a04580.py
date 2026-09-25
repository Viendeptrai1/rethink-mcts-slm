import sys
from collections import Counter

def find_divisors(n):
    divisors = set()
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            divisors.add(i)
            divisors.add(n // i)
    return divisors

def restore_numbers(n, divisors):
    counter = Counter(divisors)
    common_divisors = [d for d, count in counter.items() if count == 2]
    x_divisors = set()
    y_divisors = set()
    
    for d in divisors:
        if d in common_divisors:
            x_divisors.add(d)
            y_divisors.add(d)
        elif len(x_divisors) < (n // 2):
            x_divisors.add(d)
        else:
            y_divisors.add(d)
    
    x = 1
    for d in x_divisors:
        x *= d
    
    y = 1
    for d in y_divisors:
        y *= d
    
    return x, y

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    divisors = list(map(int, data[1:]))
    
    x, y = restore_numbers(n, divisors)
    print(x, y)

if __name__ == "__main__":
    main()