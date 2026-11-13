from itertools import product

def count_good_plans(n, m, b, mod, a):
    def is_good_plan(plan):
        total_bugs = sum(plan[i] * a[i] for i in range(n))
        return total_bugs <= b
    
    count = 0
    for plan in product(range(m+1), repeat=n):
        if sum(plan) == m and is_good_plan(plan):
            count += 1
    
    return count % mod

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
b = int(data[2])
mod = int(data[3])
a = list(map(int, data[4:]))

# Output result
print(count_good_plans(n, m, b, mod, a))