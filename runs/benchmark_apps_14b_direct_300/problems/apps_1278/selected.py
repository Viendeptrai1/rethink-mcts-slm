import sys

def find_earliest_not_so_rainy_day(n, x, y, a):
    # Initialize the result with a large value
    result = float('inf')
    
    # Iterate through each day in the summer
    for d in range(n):
        # Check if the current day is not-so-rainy
        is_not_so_rainy = True
        for j in range(max(0, d - x), d):
            if a[d] >= a[j]:
                is_not_so_rainy = False
                break
        for j in range(d + 1, min(n, d + y + 1)):
            if a[d] >= a[j]:
                is_not_so_rainy = False
                break
        
        # Update the result if the current day is not-so-rainy and earlier than the previous result
        if is_not_so_rainy and d < result:
            result = d
    
    return result + 1  # Convert zero-based index to one-based index

# Read input from standard input
input = sys.stdin.read
data = input().split()

n = int(data[0])
x = int(data[1])
y = int(data[2])
a = list(map(int, data[3:]))

# Find and print the earliest not-so-rainy day
print(find_earliest_not_so_rainy_day(n, x, y, a))