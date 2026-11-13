import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = [int(data[i+1]) for i in range(n)]
    
    # We will use a set to keep track of current prefix sums of the "clean" segments
    # that we have not broken yet.
    # Let current_prefix_sum be the sum of elements in the current valid segment we are building.
    # We also maintain a set 'seen' of all prefix sums relative to the start of the current valid segment.
    # If adding a new element would create a subsegment sum of 0 (i.e., current_prefix_sum + x == some value in seen),
    # then we must insert a separator before this element.
    
    count_insertions = 0
    current_sum = 0
    seen = set()
    seen.add(0)
    
    for x in a:
        # Check if adding x would create a zero sum subsegment
        # A zero sum subsegment ending at this position exists if there is a prefix sum P in 'seen'
        # such that P + x = 0 => P = -x.
        # Wait, the definition of subsegment sum from i to j is prefix[j] - prefix[i-1].
        # If we are maintaining prefix sums relative to the start of the current valid block:
        # Let the current block start with sum 0 (virtual).
        # The values in 'seen' are prefix sums of the current block.
        # If we add x, the new prefix sum becomes current_sum + x.
        # A subsegment sum of 0 exists if there is a previous prefix sum P in 'seen' such that:
        # (current_sum + x) - P = 0 => P = current_sum + x.
        
        if (current_sum + x) in seen:
            # We need to insert an element to break this.
            # Effectively, we close the current segment and start a new one with the current element x.
            # The insertion breaks the continuity, so the new segment starts fresh.
            count_insertions += 1
            # Reset for the new segment
            current_sum = 0
            seen.clear()
            seen.add(0)
            # Now add x to the new segment
            current_sum += x
            seen.add(current_sum)
        else:
            current_sum += x
            seen.add(current_sum)
            
    print(count_insertions)

if __name__ == '__main__':
    solve()