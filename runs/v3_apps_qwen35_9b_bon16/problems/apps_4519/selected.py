import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    idx = 0
    q = int(data[idx])
    idx += 1
    
    results = []
    
    for _ in range(q):
        n = int(data[idx])
        k = int(data[idx+1])
        s = data[idx+2]
        idx += 3
        
        # We will build the result string character by character
        # We want to place the leftmost available '0' as early as possible
        
        # Convert string to a list for mutability (though we rebuild logic)
        # Actually, we can simulate the process:
        # Iterate through positions i from 0 to n-1
        # Try to find the nearest '0' that can be moved to position i with cost <= remaining k
        
        s_list = list(s)
        res = []
        
        # Pointer to the next character we are considering moving
        # We look for '0's to bring forward
        # Strategy: For each position i in the result, try to bring the closest available '0' to i
        # The cost is the number of swaps, which equals the distance between the '0' and position i,
        # minus the number of characters already skipped over that are also '0' (but those would have been used).
        # Actually, simpler: The cost to move a specific '0' from its current index to target index i
        # is exactly (current_index - i), provided we move it past all intervening characters.
        # Since we process from left to right, we maintain the current index of the next '0' candidate.
        
        # Let's find all indices of '0's first
        zero_indices = [i for i, c in enumerate(s_list) if c == '0']
        zero_idx_ptr = 0
        
        current_pos = 0
        
        for i in range(n):
            # We want to decide what character goes at position i
            # Ideally a '0' if we can afford it.
            # Check if there is a '0' available that can be moved to i within budget k
            
            # The candidate '0' is at zero_indices[zero_idx_ptr]
            if zero_idx_ptr < len(zero_indices):
                z_pos = zero_indices[zero_idx_ptr]
                cost = z_pos - i
                
                if cost <= k:
                    # We can move this '0' to position i
                    # Append '0' to result
                    res.append('0')
                    # Consume this zero
                    zero_idx_ptr += 1
                    # Update k
                    k -= cost
                else:
                    # We cannot move this '0' to position i.
                    # Since this is the leftmost available '0' and we can't reach i,
                    # we definitely can't reach any subsequent '0' either (they are even further).
                    # So we must put '1' at this position.
                    res.append('1')
            else:
                # No more '0's available, must be '1'
                res.append('1')
        
        results.append("".join(res))
    
    print("\n".join(results))

if __name__ == "__main__":
    solve()