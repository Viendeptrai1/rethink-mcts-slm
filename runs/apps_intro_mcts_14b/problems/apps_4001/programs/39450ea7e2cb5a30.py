import sys
from collections import Counter

def find_x_y(n, divisors):
    # Sort the divisors in descending order
    divisors.sort(reverse=True)
    
    # The largest number in the sorted list is a candidate for x or y
    x_candidate = divisors[0]
    y_candidate = divisors[1]
    
    # Check if the candidates are valid by comparing the counts of divisors
    def count_divisors(num):
        count = Counter()
        for i in range(1, int(num**0.5) + 1):
            if num % i == 0:
                count[i] += 1
                if i != num // i:
                    count[num // i] += 1
        return count
    
    x_count = count_divisors(x_candidate)
    y_count = count_divisors(y_candidate)
    
    # Merge the counts and compare with the original list's count
    merged_count = x_count + y_count
    original_count = Counter(divisors)
    
    # Adjust the candidates if necessary
    if merged_count != original_count:
        x_candidate, y_candidate = y_candidate, x_candidate
        x_count = count_divisors(x_candidate)
        y_count = count_divisors(y_candidate)
        merged_count = x_count + y_count
    
    return x_candidate, y_candidate

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
divisors = list(map(int, data[1:]))

# Find x and y
x, y = find_x_y(n, divisors)

# Print the result
print(x, y)