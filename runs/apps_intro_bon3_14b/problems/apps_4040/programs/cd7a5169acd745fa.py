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
        while current_position < n and a[current_position] != 0:
            current_position += 1
        
        # Place the platform
        for j in range(c[i]):
            if current_position + j >= n:
                return "NO", []
            a[current_position + j] = i + 1
        
        # Move to the next possible starting position for the next platform
        current_position += c[i]

    # Check if we can reach the end from the last platform
    last_platform_end = current_position - 1
    for i in range(last_platform_end, n):
        if a[i] != 0:
            last_platform_end = i
    
    # Try to jump from the last platform to the end
    current_position = last_platform_end
    while current_position < n:
        found_jump = False
        for jump in range(1, d + 1):
            if current_position + jump <= n and a[current_position + jump] != 0:
                current_position += jump
                found_jump = True
                break
        if not found_jump:
            return "NO", []

    return "YES", a

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