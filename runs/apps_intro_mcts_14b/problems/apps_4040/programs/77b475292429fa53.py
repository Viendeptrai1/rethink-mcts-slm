import sys

def can_reach_end(n, m, d, c):
    # Sort platforms by length in descending order
    c.sort(reverse=True)
    
    # Initialize the river with 0s
    river = [0] * (n + 2)
    
    # Place platforms starting from the left bank
    current_position = 1
    for i in range(m):
        # Place the i-th platform
        for j in range(c[i]):
            river[current_position + j] = i + 1
        # Move to the next possible position
        current_position += c[i] + 1
    
    # Check if we can reach the right bank
    current_position = 0
    visited = set()
    while current_position <= n + 1:
        if current_position == n + 1:
            return "YES", river[1:n+1]
        if current_position in visited:
            break
        visited.add(current_position)
        # Try to jump to the next possible position
        for next_position in range(current_position + 1, min(current_position + d + 1, n + 2)):
            if river[next_position] != 0:
                current_position = next_position
                break
        else:
            break
    
    return "NO", []

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    d = int(data[2])
    c = list(map(int, data[3:3+m]))
    
    result, river = can_reach_end(n, m, d, c)
    print(result)
    if result == "YES":
        print(" ".join(map(str, river)))

if __name__ == "__main__":
    main()