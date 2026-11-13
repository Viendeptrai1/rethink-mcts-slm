import sys

def generate_permutation(n, k):
    if k == 0:
        return list(range(1, n + 1))
    elif k == n - 1:
        return list(range(n, 0, -1))
    
    permutation = list(range(1, n + 1))
    swap_count = 0
    
    # Perform swaps to achieve the desired decreasing coefficient
    for i in range(n - 1, 0, -1):
        if swap_count >= k:
            break
        permutation[i], permutation[i - 1] = permutation[i - 1], permutation[i]
        swap_count += 1
    
    return permutation

# Read input
input_line = sys.stdin.readline().strip()
n, k = map(int, input_line.split())

# Generate and print the permutation
result = generate_permutation(n, k)
print(" ".join(map(str, result)))