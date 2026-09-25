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
    
    # Count the frequency of each divisor
    freq = Counter(divisors_list)
    
    # Find the most frequent elements, they are likely to be common divisors
    common_divisors = [k for k, v in freq.items() if v > 1]
    
    # Try to find x and y
    for i in range(len(common_divisors)):
        for j in range(i, len(common_divisors)):
            d = common_divisors[i]
            e = common_divisors[j]
            x_divisors = find_divisors(d)
            y_divisors = find_divisors(e)
            
            # Combine divisors with duplicates for common divisors
            combined_divisors = list(x_divisors) + list(y_divisors)
            combined_divisors.sort()
            
            # Check if the combined divisors match the given list
            if sorted(combined_divisors) == sorted(divisors_list):
                print(d, e)
                return

if __name__ == "__main__":
    main()