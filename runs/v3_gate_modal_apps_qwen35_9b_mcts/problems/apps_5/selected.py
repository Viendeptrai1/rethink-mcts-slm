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
    
    # Strategy 1: Close left side first, then right side
    cost1 = 0
    if l > 1:
        # Move from pos to l
        cost1 += abs(pos - l)
        # Close left side (cost 1)
        cost1 += 1
        # Now we are at l. We need to go to r+1 to close the right side.
        # Note: After closing left, the new 'a' becomes l, but the cursor is at l.
        # To close right side [i+1, b], we need to be at i such that i+1 is the start of the right segment to close?
        # Actually, the operation is: at tab i, close [i+1, b]. So to close everything to the right of r,
        # we need to be at tab r. Then closing [r+1, b] removes everything > r.
        # So we move from l to r.
        cost1 += abs(l - r)
        # Close right side
        cost1 += 1
    else:
        # l == 1, no need to close left. Just close right.
        # Move from pos to r
        cost1 += abs(pos - r)
        # Close right side
        cost1 += 1
    
    # Strategy 2: Close right side first, then left side
    cost2 = 0
    if r < n:
        # Move from pos to r
        cost2 += abs(pos - r)
        # Close right side
        cost2 += 1
        # Now we are at r. We need to go to l to close the left side.
        # To close left side [a, i-1], we need to be at tab l+1? 
        # Wait, to close [a, i-1], if we want to close everything < l, we need the segment to be [1, l-1].
        # So we need i-1 = l-1 => i = l.
        # So we move from r to l.
        cost2 += abs(r - l)
        # Close left side
        cost2 += 1
    else:
        # r == n, no need to close right. Just close left.
        # Move from pos to l
        cost2 += abs(pos - l)
        # Close left side
        cost2 += 1
    
    print(min(cost1, cost2))

if __name__ == "__main__":
    solve()