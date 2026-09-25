import sys
from collections import Counter

def get_divisors(n):
    divisors = set()
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            divisors.add(i)
            divisors.add(n // i)
    return divisors

def find_x_y(divisors_list):
    n = len(divisors_list)
    divisors_count = Counter(divisors_list)
    divisors = sorted(divisors_count.keys())
    
    for i in range(len(divisors)):
        for j in range(i, len(divisors)):
            x = divisors[i]
            y = divisors[j]
            x_divisors = get_divisors(x)
            y_divisors = get_divisors(y)
            combined_divisors = Counter()
            
            for d in x_divisors:
                combined_divisors[d] += 1
            for d in y_divisors:
                combined_divisors[d] += 1
            
            if combined_divisors == divisors_count:
                return x, y

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    divisors_list = list(map(int, data[1:]))
    
    x, y = find_x_y(divisors_list)
    print(x, y)

if __name__ == "__main__":
    main()