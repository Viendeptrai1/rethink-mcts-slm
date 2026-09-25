import sys

def can_reach_end(n, m, d, c):
    # Check if the total length of platforms is less than or equal to n
    if sum(c) > n:
        return "NO", []

    # Initialize the array to store the platform positions
    a = [0] * n

    # Try to place the platforms in a way that allows reaching the end
    current_position = 0
    for i in range(m):
        # Find the next available position to place the platform
        while current_position + c[i] - 1 >= n or any(a[current_position:current_position + c[i]] != [0] * c[i]):
            current_position += 1
        
        # Place the platform
        for j in range(c[i]):
            a[current_position + j] = i + 1
        
        # Move to the next possible starting position for the next platform
        current_position += c[i]

    # Check if we can reach the end from the last platform
    last_platform_end = current_position - 1
    reachable = False
    for i in range(last_platform_end, n):
        if a[i] != 0:
            reachable = True
            break

    if not reachable:
        return "NO", []

    # Check if we can jump from the last platform to the end
    for i in range(last_platform_end, n):
        if a[i] != 0:
            if i + d > n:
                return "YES", a
            if any(a[i + 1:i + d + 1] == [0] * (d + 1)):
                return "YES", a

    return "NO", []

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
d = int(data[2])
c = list(map(int, data[3:]))

# Solve the problem
result, a = can_reach_end(n, m, d, c)

# Print the result
print(result)
if result == "YES":
    print(" ".join(map(str, a)))