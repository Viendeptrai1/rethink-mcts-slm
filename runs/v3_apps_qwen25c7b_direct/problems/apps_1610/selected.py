def generate_permutation(n, k):
    if k == 0:
        return list(range(1, n + 1))
    elif k == n - 1:
        return list(reversed(range(1, n + 1)))
    
    result = [i for i in range(1, n + 1)]
    swaps = k
    
    while swaps > 0:
        for i in range(n - 1, 0, -1):
            if result[i] < result[i - 1]:
                result[i], result[i - 1] = result[i - 1], result[i]
                swaps -= 1
                break
    
    return result

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])

# Generate and print the permutation
permutation = generate_permutation(n, k)
print(' '.join(map(str, permutation)))