import sys

def can_reach_end(n, m, d, c):
    # Initialize the array to store the platform placement
    a = [0] * n
    
    # Try to place the platforms in a way that maximizes reachable positions
    current_position = 0
    for i in range(m):
        # Place the i-th platform starting from the current position
        for j in range(c[i]):
            a[current_position + j] = i + 1
        # Move to the next possible position where we can place the next platform
        current_position += c[i]
    
    # Check if we can reach from 0 to n+1
    reachable = [False] * (n + 2)
    reachable[0] = True
    
    for i in range(n + 2):
        if reachable[i]:
            for j in range(1, d + 1):
                if i + j <= n + 1 and a[i + j - 1] != 0:
                    reachable[i + j] = True
    
    if reachable[n + 1]:
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
    c = list(map(int, data[3:3 + m]))
    
    result, a = can_reach_end(n, m, d, c)
    print(result)
    if result == "YES":
        print(" ".join(map(str, a)))

if __name__ == "__main__":
    main()