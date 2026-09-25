import sys

def can_reach_end(n, m, d, c):
    # Check if the total length of platforms is less than or equal to n
    if sum(c) > n:
        return "NO", []

    # Initialize the positions of platforms
    positions = [0] * (n + 2)
    current_position = 1

    # Place the platforms
    for i in range(m):
        while current_position + c[i] - 1 > n:
            current_position += 1
        for j in range(current_position, current_position + c[i]):
            positions[j] = i + 1
        current_position += c[i]

    # Check if we can reach from 0 to n+1
    current_cell = 0
    visited = [False] * (n + 2)
    visited[0] = True

    while current_cell != n + 1:
        found = False
        for next_cell in range(current_cell + 1, min(current_cell + d + 1, n + 2)):
            if positions[next_cell] != 0 and not visited[next_cell]:
                visited[next_cell] = True
                current_cell = next_cell
                found = True
                break
        if not found:
            return "NO", []

    # Construct the result array
    result = [positions[i] for i in range(1, n + 1)]
    return "YES", result

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
d = int(data[2])
c = list(map(int, data[3:]))

# Get the result
result_status, result_array = can_reach_end(n, m, d, c)

# Print the result
print(result_status)
if result_status == "YES":
    print(" ".join(map(str, result_array)))