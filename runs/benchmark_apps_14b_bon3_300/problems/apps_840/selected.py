import sys
import heapq

def max_cookies(n, k, a, b):
    # Calculate the deficit for each ingredient
    deficit = []
    for i in range(n):
        if b[i] < a[i]:
            deficit.append(a[i] - b[i])
    
    # If there's no deficit, we can bake as many cookies as possible with the magic powder
    if not deficit:
        return k // min(a)
    
    # Use a max-heap to keep track of the largest deficits
    heapq.heapify(deficit)
    
    # Try to reduce the deficit using the magic powder
    while k > 0 and deficit:
        largest_deficit = heapq.heappop(deficit)
        if k >= largest_deficit:
            k -= largest_deficit
        else:
            break
    
    # Calculate the maximum number of cookies we can bake now
    total_ingredients = sum(min(a[i], b[i] + (k if i == 0 else 0)) for i in range(n))
    return total_ingredients // min(a)

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:2+n]))
b = list(map(int, data[2+n:]))

# Output the result
print(max_cookies(n, k, a, b))