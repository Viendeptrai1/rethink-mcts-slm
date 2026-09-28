import sys
from collections import Counter

def find_numbers(n, divisors):
    # Count the occurrences of each divisor
    divisor_counts = Counter(divisors)
    
    # Find the maximum divisor
    max_divisor = max(divisors)
    
    # Initialize x and y as 1
    x = 1
    y = 1
    
    # Iterate over the unique divisors
    for divisor, count in divisor_counts.items():
        if count == 1:
            # If a divisor appears only once, it must belong to one of the numbers
            if x == 1:
                x = divisor
            else:
                y = divisor
        elif count == 2:
            # If a divisor appears twice, it is a common divisor
            x *= divisor
            y *= divisor
    
    return x, y

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    divisors = list(map(int, data[1:]))
    
    x, y = find_numbers(n, divisors)
    print(x, y)

if __name__ == "__main__":
    main()