import sys

def can_reach_end(n, m, d, c):
    # Check if it's possible to place platforms such that we can jump from 0 to n+1
    if sum(c) == n:
        # If the total length of platforms equals the width of the river, we can place them consecutively
        return True
    if max(c) > d:
        # If any platform is longer than the maximum jump distance, it's impossible to place them without gaps
        return False
    return True

def find_platform_placement(n, m, d, c):
    # Initialize the river with 0s
    river = [0] * (n + 2)
    
    # Place the platforms starting from the left bank
    current_position = 1
    for i in range(m):
        # Place the i-th platform starting from current_position
        for j in range(c[i]):
            river[current_position + j] = i + 1
        # Move to the next possible position after placing the current platform
        current_position += c[i] + 1
    
    # Remove the first and last elements (0 and n+1) as they are not part of the output
    river = river[1:-1]
    
    return river

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    d = int(data[2])
    c = list(map(int, data[3:]))
    
    if can_reach_end(n, m, d, c):
        river = find_platform_placement(n, m, d, c)
        print("YES")
        print(" ".join(map(str, river)))
    else:
        print("NO")

if __name__ == "__main__":
    main()