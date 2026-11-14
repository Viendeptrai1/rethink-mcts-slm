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
        
        # Convert string to a list of characters for mutability
        chars = list(s)
        # Track the next available '0' index
        next_zero = -1
        
        # We will build the result string character by character
        # But to avoid O(n^2) scanning, we pre-scan for zeros
        zero_indices = [i for i, c in enumerate(chars) if c == '0']
        zero_ptr = 0
        
        res = []
        
        for i in range(n):
            # Try to place a '0' at position i if possible
            if zero_ptr < len(zero_indices):
                zero_pos = zero_indices[zero_ptr]
                
                # Calculate cost to move zero_pos to i
                # The cost is the number of swaps, which is (zero_pos - i)
                # However, we must ensure that all characters between i and zero_pos
                # are shifted right. Since we are building the result from left to right,
                # the actual cost is simply the distance in the current conceptual string.
                # But wait, the problem allows swapping adjacent characters.
                # Moving a '0' from index `zero_pos` to `i` requires `zero_pos - i` swaps
                # ONLY IF there are no other '0's already moved from between i and zero_pos.
                # Since we process left to right and greedily take the nearest '0',
                # any '0' we skipped is still to the right of the current `zero_pos`.
                # Any '1's between i and zero_pos need to be swapped past.
                # The number of swaps is exactly (zero_pos - i) because we are moving
                # the '0' leftwards past all characters currently at indices i, i+1, ..., zero_pos-1.
                
                cost = zero_pos - i
                
                if k >= cost:
                    # We can move this '0' to position i
                    res.append('0')
                    k -= cost
                    zero_ptr += 1
                else:
                    # We cannot move this '0' to position i.
                    # This '0' will stay at its relative position or be moved later?
                    # Actually, if we can't move the nearest '0' to `i`, we can't move any
                    # subsequent '0' to `i` either because they are even further away.
                    # So position `i` must be filled with a '1'.
                    res.append('1')
                    # The '0' at zero_pos remains in the pool for future positions.
                    # Its effective index in the remaining string decreases as we fill '1's,
                    # but the cost calculation `zero_pos - i` accounts for the current state.
                    # We do NOT increment zero_ptr.
            else:
                # No more '0's available, fill with '1'
                res.append('1')
        
        results.append("".join(res))
    
    print("\n".join(results))

if __name__ == "__main__":
    solve()