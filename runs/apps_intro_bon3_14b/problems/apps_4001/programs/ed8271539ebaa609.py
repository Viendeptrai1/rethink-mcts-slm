import sys
from collections import Counter

def find_divisors(n):
    divisors = set()
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            divisors.add(i)
            divisors.add(n // i)
    return divisors

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    divisors_list = list(map(int, data[1:]))
    
    counter = Counter(divisors_list)
    common_divisors = [d for d, count in counter.items() if count == 2]
    unique_divisors = [d for d, count in counter.items() if count == 1]
    
    x_divisors = set(common_divisors)
    y_divisors = set(common_divisors)
    
    for d in unique_divisors:
        if len(x_divisors) < len(y_divisors):
            x_divisors.add(d)
        else:
            y_divisors.add(d)
    
    x = 1
    for d in x_divisors:
        x *= d
    
    y = 1
    for d in y_divisors:
        y *= d
    
    print(x, y)

if __name__ == "__main__":
    main()