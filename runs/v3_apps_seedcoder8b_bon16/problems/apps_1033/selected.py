def min_spots(n, H):
    left = 0
    right = n
    while left < right:
        mid = (left + right) // 2
        total = (mid * (mid + 1)) // 2 + max(0, mid - H)
        if total >= n:
            right = mid
        else:
            left = mid + 1
    return left

# Read input
n, H = map(int, input().split())

# Calculate and print the result
result = min_spots(n, H)
print(result)