import sys

def can_reach_end(n, m, d, c):
    # Initialize the array to store the platform positions
    a = [0] * n
    
    # Try to place each platform in the leftmost possible position
    current_position = 0
    for i in range(m):
        # Find the leftmost position to place the i-th platform
        while current_position + c[i] > n + 1 or (current_position > 0 and a[current_position - 1] == i + 1):
            current_position += 1
        
        # Place the platform
        for j in range(c[i]):
            a[current_position + j] = i + 1
        
        # Update the current position to the end of the current platform
        current_position += c[i]
    
    # Check if we can reach the end
    current_position = 0
    for i in range(n):
        if a[i] != 0:
            current_position = i + 1
        if current_position + d > n + 1:
            break
    
    if current_position + d >= n + 1:
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