import sys
from collections import Counter

def find_numbers(n, divisors):
    # Count the frequency of each divisor
    divisor_count = Counter(divisors)
    
    # Find the maximum divisor
    max_divisor = max(divisors)
    
    # Initialize x and y as 1
    x = 1
    y = 1
    
    # Iterate over each unique divisor
    for divisor in divisor_count:
        # If the divisor appears twice, it is a common divisor
        if divisor_count[divisor] == 2:
            x *= divisor
            y *= divisor
        elif divisor_count[divisor] == 1:
            # If the divisor appears once, it belongs to one of the numbers
            if x % divisor != 0:
                x *= divisor
            else:
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