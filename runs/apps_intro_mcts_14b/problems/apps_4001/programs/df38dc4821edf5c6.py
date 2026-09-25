import sys
from collections import Counter

def get_divisors(n):
    divisors = set()
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            divisors.add(i)
            divisors.add(n // i)
    return divisors

def find_xy(n, divisors):
    for i in range(n):
        for j in range(i + 1, n):
            x = divisors[i]
            y = divisors[j]
            x_divs = get_divisors(x)
            y_divs = get_divisors(y)
            combined_divs = Counter(x_divs) + Counter(y_divs)
            if combined_divs == Counter(divisors):
                return x, y
    return None, None

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    divisors = list(map(int, data[1:]))
    
    x, y = find_xy(n, divisors)
    print(x, y)

if __name__ == "__main__":
    main()