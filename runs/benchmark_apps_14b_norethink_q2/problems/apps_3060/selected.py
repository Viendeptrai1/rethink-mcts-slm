def find_kth_sequence(n, k):
    from functools import lru_cache
    
    @lru_cache(None)
    def count_sequences(length, remainder):
        if length == 0:
            return 1 if remainder != 0 else 0
        total = 0
        for petals in range(1, n):
            new_remainder = (remainder + petals) % n
            total += count_sequences(length - 1, new_remainder)
        return total
    
    @lru_cache(None)
    def find_sequence(length, remainder, k):
        if length == 0:
            return []
        for petals in range(1, n):
            new_remainder = (remainder + petals) % n
            count = count_sequences(length - 1, new_remainder)
            if k <= count:
                return [petals] + find_sequence(length - 1, new_remainder, k)
            k -= count
    
    return find_sequence(n - 1, 0, k)

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])

# Find and print the k-th sequence
result = find_kth_sequence(n, k)
print(' '.join(map(str, result)))