from collections import defaultdict

def calculate_f(x):
    if x == 0:
        return 0
    elif x % 2 == 0:
        return calculate_f(x // 2)
    else:
        return calculate_f(x // 2) + 1

def count_pairs(n, a):
    f_values = defaultdict(int)
    for num in a:
        f_values[calculate_f(num)] += 1
    
    total_pairs = 0
    for count in f_values.values():
        total_pairs += count * (count - 1) // 2
    
    return total_pairs

# Input reading
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

# Output the result
print(count_pairs(n, a))