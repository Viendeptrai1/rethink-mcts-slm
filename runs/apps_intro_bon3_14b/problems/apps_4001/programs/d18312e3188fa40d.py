import sys
from collections import Counter

def find_numbers(n, divisors):
    # Count the frequency of each divisor
    freq = Counter(divisors)
    
    # Find the maximum divisor which will be one of the numbers
    max_divisor = max(freq.keys())
    
    # The other number will be the product of all divisors divided by the max_divisor
    other_number = 1
    for divisor in freq:
        if divisor != max_divisor:
            other_number *= divisor ** (freq[divisor] // 2)
    
    return max_divisor, other_number

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