import sys

def can_reach_end(n, m, d, c):
    # Initialize the array to store the placement of platforms
    a = [0] * n
    
    # Try to place the platforms in a way that maximizes reachable positions
    current_position = 0
    for i in range(m):
        # Place the i-th platform starting from the current position
        for j in range(c[i]):
            a[current_position + j] = i + 1
        # Move to the next possible position after placing the current platform
        current_position += c[i]
    
    # Check if we can reach the end from the start
    current_position = 0
    visited = set()
    while current_position < n:
        if current_position in visited:
            break
        visited.add(current_position)
        # Try to jump to the next possible position
        next_position = current_position + 1
        while next_position <= min(current_position + d, n - 1) and a[next_position] == 0:
            next_position += 1
        if next_position > n or a[next_position] == 0:
            break
        current_position = next_position
    
    # If we reached the end, return the placement array
    if current_position >= n:
        return "YES", a
    else:
        return "NO", []

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    d = int(data[2])
    c = list(map(int, data[3:3+m]))
    
    result, a = can_reach_end(n, m, d, c)
    print(result)
    if result == "YES":
        print(" ".join(map(str, a)))

if __name__ == "__main__":
    main()