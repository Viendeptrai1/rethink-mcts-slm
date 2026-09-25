import sys

def can_reach_end(n, m, d, c):
    # Check if we can reach the end with the given constraints
    if d >= n:
        return "YES", [0] * n
    
    # Initialize the positions of the platforms
    positions = [0] * (n + 2)
    positions[0] = 1
    positions[n + 1] = 1
    
    # Try to place the platforms
    current_position = 1
    for i in range(m):
        placed = False
        while not placed:
            if current_position + c[i] - 1 <= n + 1:
                for j in range(current_position, current_position + c[i]):
                    if positions[j] != 0:
                        break
                else:
                    for j in range(current_position, current_position + c[i]):
                        positions[j] = i + 1
                    placed = True
            else:
                break
            current_position += 1
    
    # Check if we can reach the end
    current_position = 0
    reachable = [False] * (n + 2)
    reachable[0] = True
    for i in range(n + 2):
        if reachable[i]:
            for j in range(i + 1, min(i + d + 1, n + 2)):
                if positions[j] != 0:
                    reachable[j] = True
    
    if reachable[n + 1]:
        result = [positions[i] for i in range(1, n + 1)]
        return "YES", result
    else:
        return "NO", []

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
m = int(data[1])
d = int(data[2])
c = list(map(int, data[3:]))

# Get the result
result_status, result_positions = can_reach_end(n, m, d, c)

# Print the result
print(result_status)
if result_status == "YES":
    print(" ".join(map(str, result_positions)))