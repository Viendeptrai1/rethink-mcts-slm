def count_numbers(N, A):
    seen = set()
    for num in A:
        if num in seen:
            seen.remove(num)
        else:
            seen.add(num)
    return len(seen)

# Read input
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
A = list(map(int, data[1:]))

# Calculate and print the result
print(count_numbers(N, A))