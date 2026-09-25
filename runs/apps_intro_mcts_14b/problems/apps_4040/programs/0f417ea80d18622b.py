import sys

def can_reach_end(n, m, d, c):
    # Check if the total length of platforms is less than or equal to n
    if sum(c) > n:
        return "NO", []

    # Initialize the river with 0s
    river = [0] * (n + 2)

    # Place platforms in the river
    current_position = 1
    for i in range(m):
        while current_position + c[i] - 1 <= n and river[current_position] != 0:
            current_position += 1
        if current_position + c[i] - 1 > n:
            return "NO", []
        for j in range(c[i]):
            river[current_position + j] = i + 1
        current_position += c[i]

    # Check if we can reach from 0 to n+1
    current_position = 0
    visited = set()
    queue = [(current_position, 0)]
    while queue:
        pos, platform = queue.pop(0)
        if pos == n + 1:
            return "YES", river[1:-1]
        if pos in visited:
            continue
        visited.add(pos)
        for jump in range(1, d + 1):
            next_pos = pos + jump
            if 0 < next_pos <= n + 1 and river[next_pos] != 0:
                queue.append((next_pos, river[next_pos]))

    return "NO", []

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
d = int(data[2])
c = list(map(int, data[3:]))

# Get the result
result, river = can_reach_end(n, m, d, c)

# Print the result
print(result)
if result == "YES":
    print(" ".join(map(str, river)))