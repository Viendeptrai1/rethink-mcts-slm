from collections import Counter
from math import factorial

MOD = 998244353

def count_good_permutations(n, s):
    def count_sorted_by_first():
        cnt = Counter(a for a, _ in s)
        return sum(factorial(v) for v in cnt.values()) % MOD
    
    def count_sorted_by_second():
        cnt = Counter(b for _, b in s)
        return sum(factorial(v) for v in cnt.values()) % MOD
    
    def count_both_sorted():
        cnt_a = Counter(a for a, _ in s)
        cnt_b = Counter(b for _, b in s)
        return sum(min(cnt_a[a], cnt_b[b]) for a, b in s) % MOD
    
    total_permutations = factorial(n)
    sorted_by_first = count_sorted_by_first()
    sorted_by_second = count_sorted_by_second()
    both_sorted = count_both_sorted()
    
    result = (total_permutations - sorted_by_first - sorted_by_second + both_sorted) % MOD
    return result

# Input reading
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
s = [(int(data[i*2+1]), int(data[i*2+2])) for i in range(n)]

# Output the result
print(count_good_permutations(n, s))