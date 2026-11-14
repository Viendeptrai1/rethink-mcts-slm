import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    R = int(input_data[0])
    C = int(input_data[1])
    K = int(input_data[2])
    
    # The hedgehog starts at (0,0) and moves in a zig-zag pattern.
    # The path is defined by the sum of coordinates s = r + c.
    # s goes from 0 upwards.
    # For a given s, the cells are (r, c) such that r + c = s, with 0 <= r < R and 0 <= c < C.
    # The order within a diagonal s depends on the parity of s:
    # - If s is even: r increases from max(0, s - (C-1)) to min(s, R-1).
    # - If s is odd: r decreases from min(s, R-1) to max(0, s - (C-1)).
    #
    # A cell (r, c) is grey if (r & c) == 0.
    # We need to count how many grey cells are visited in the first K steps.
    
    count = 0
    steps = 0
    s = 0
    
    while steps < K:
        # Determine the range of r for the current diagonal s
        # Constraints: 0 <= r < R and 0 <= c < C => 0 <= r < R and 0 <= s-r < C => s-C+1 <= r <= s
        r_min = max(0, s - C + 1)
        r_max = min(s, R - 1)
        
        if r_min > r_max:
            # This diagonal has no cells on the board
            s += 1
            continue
        
        # Determine the number of cells in this diagonal
        num_cells = r_max - r_min + 1
        
        # Determine how many cells we can take from this diagonal
        take = min(num_cells, K - steps)
        
        # Iterate through the cells in the correct order for this diagonal
        if s % 2 == 0:
            # Even s: r increases
            for r in range(r_min, r_min + take):
                c = s - r
                if (r & c) == 0:
                    count += 1
        else:
            # Odd s: r decreases
            # We need to iterate 'take' times starting from r_max downwards
            for i in range(take):
                r = r_max - i
                c = s - r
                if (r & c) == 0:
                    count += 1
        
        steps += take
        s += 1
        
        if steps >= K:
            break
            
    print(count)

if __name__ == "__main__":
    solve()