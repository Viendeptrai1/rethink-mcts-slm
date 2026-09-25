import sys

def can_complete_wall(n, a):
    # Find the minimum height in the wall
    min_height = min(a)
    
    # Check if we can make all parts of the wall have the same height
    for i in range(n - 1):
        if a[i] < a[i + 1]:
            # If the current part is less than the next part, we need to check if we can make them equal
            if (a[i + 1] - a[i]) % 2 != 0:
                return "NO"
            # We can add bricks to make them equal
            a[i] += (a[i + 1] - a[i]) // 2
            a[i + 1] -= (a[i + 1] - a[i]) // 2
    
    # After processing, all parts should have the same height
    return "YES" if all(x == min_height for x in a) else "NO"

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:]))

# Output the result
print(can_complete_wall(n, a))