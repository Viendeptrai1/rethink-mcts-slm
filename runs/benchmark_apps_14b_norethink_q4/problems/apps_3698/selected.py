MOD = 10**9 + 7

def count_special_numbers(n, k):
    def count_operations(x):
        count = 0
        while x > 1:
            x = bin(x).count('1')
            count += 1
        return count

    special_count = 0
    for i in range(1, int(n, 2) + 1):
        if count_operations(i) == k:
            special_count += 1
            special_count %= MOD

    return special_count

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = data[0]
k = int(data[1])

# Output the result
print(count_special_numbers(n, k))