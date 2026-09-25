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
    
    # Count the occurrences of each divisor
    divisor_counts = Counter(divisors_list)
    
    # Find unique divisors
    unique_divisors = sorted(divisor_counts.keys(), reverse=True)
    
    # Initialize x and y with the largest unique divisor
    x = unique_divisors[0]
    y = unique_divisors[1]
    
    # Remove the divisors of x and y from the count
    x_divisors = find_divisors(x)
    y_divisors = find_divisors(y)
    
    for d in x_divisors:
        divisor_counts[d] -= 1
    for d in y_divisors:
        divisor_counts[d] -= 1
    
    # Adjust x and y based on remaining counts
    for d in unique_divisors[2:]:
        if divisor_counts[d] > 0:
            if d in x_divisors:
                y *= d
            else:
                x *= d
    
    print(x, y)

if __name__ == "__main__":
    main()