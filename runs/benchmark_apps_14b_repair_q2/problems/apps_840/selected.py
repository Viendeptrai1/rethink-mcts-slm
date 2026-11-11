import sys
import heapq

def max_cookies(n, k, a, b):
    # Calculate the difference between what we have and what we need for each ingredient
    diff = [b_i - a_i for a_i, b_i in zip(a, b)]
    
    # We want to maximize the number of cookies, so we should try to use as much of the magic powder as possible
    # This means we should prioritize using the ingredients where we have more than we need
    # We can use a min-heap to keep track of the smallest differences
    heapq.heapify(diff)
    
    # The number of cookies we can bake is determined by the ingredient with the smallest difference
    # We can bake as many cookies as the minimum of the magic powder divided by this difference
    # If the difference is negative, it means we don't have enough of that ingredient, so we can't bake any cookies
    if all(d <= 0 for d in diff):
        return 0
    
    # Find the minimum positive difference
    min_positive_diff = min(d for d in diff if d > 0)
    
    # The maximum number of cookies we can bake is the magic powder divided by this minimum difference
    return k // min_positive_diff

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:2+n]))
b = list(map(int, data[2+n:2+2*n]))

# Print the result
print(max_cookies(n, k, a, b))