import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    pos = int(input_data[1])
    l = int(input_data[2])
    r = int(input_data[3])
    
    # If the current range [l, r] already covers all tabs (1 to n), no action needed
    if l == 1 and r == n:
        print(0)
        return
    
    # Calculate distance to boundaries
    dist_left = abs(pos - l)
    dist_right = abs(pos - r)
    
    # Option 1: Go left first, then right
    # Move from pos to l, close left, then move from l to r, close right
    cost1 = dist_left + 1 + dist_right + 1
    
    # Option 2: Go right first, then left
    # Move from pos to r, close right, then move from r to l, close left
    cost2 = dist_right + 1 + dist_left + 1
    
    print(min(cost1, cost2))

if __name__ == "__main__":
    solve()