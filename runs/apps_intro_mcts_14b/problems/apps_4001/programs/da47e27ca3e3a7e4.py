import sys
from collections import Counter

def get_divisors(n):
    divisors = set()
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            divisors.add(i)
            divisors.add(n // i)
    return divisors

def find_x_y(n, divisors_list):
    counter = Counter(divisors_list)
    unique_divisors = list(counter.keys())
    
    for i in range(len(unique_divisors)):
        for j in range(i, len(unique_divisors)):
            x = unique_divisors[i]
            y = unique_divisors[j]
            x_divisors = get_divisors(x)
            y_divisors = get_divisors(y)
            combined_divisors = x_divisors.union(y_divisors)
            combined_count = Counter(d for d in combined_divisors for _ in range((x % d == 0) + (y % d == 0)))
            
            if combined_count == counter:
                return x, y

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    divisors_list = list(map(int, data[1:]))
    
    x, y = find_x_y(n, divisors_list)
    print(x, y)

if __name__ == "__main__":
    main()