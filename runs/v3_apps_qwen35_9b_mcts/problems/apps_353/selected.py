import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    a = list(map(int, input_data[1:n+1]))

    if n == 1:
        # With only one day, we cannot determine direction unless it's 0 or 15?
        # Actually, if a[0] is 0, next must be 1 (UP).
        # If a[0] is 15, next must be 14 (DOWN).
        # If a[0] is anything else (1..14), it could be going up or down.
        if a[0] == 0:
            print("UP")
        elif a[0] == 15:
            print("DOWN")
        else:
            print("-1")
        return

    # Check transitions
    # The cycle is: 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1
    # We need to see if the sequence is strictly increasing, strictly decreasing, or ambiguous.
    
    # Let's check the last transition
    last_val = a[-1]
    prev_val = a[-2]
    
    # Determine if the sequence so far is consistent with UP or DOWN
    # UP means the sequence was increasing: ... x, x+1, ...
    # DOWN means the sequence was decreasing: ... x, x-1, ...
    
    # Check if the last step was UP
    was_up = (last_val > prev_val)
    # Check if the last step was DOWN
    was_down = (last_val < prev_val)
    
    # If equal, that's impossible per problem statement (consistent data), so ignore.
    
    if was_up:
        # The moon was increasing. Next could be UP or DOWN depending on current value.
        if last_val == 15:
            # Must be DOWN
            print("DOWN")
        elif last_val == 0:
            # Impossible to reach 0 and then go up in this context unless it's the start of cycle, 
            # but if we were going up and hit 0, the previous must have been -1 which is impossible.
            # So if we are at 0 and came from UP, it's invalid input, but problem guarantees consistency.
            # Actually, if we are at 0, the only way to get there is from 1 (DOWN). 
            # So if we see ... 1, 0, then was_up is False.
            # Thus, if was_up is True, last_val cannot be 0.
            print("UP") # Should not happen logically if consistent
        else:
            # Could be UP (if not 15) or DOWN (if next is 15? No, if not 15, next is last_val+1)
            # Wait, if we are at 8 and came from 7, next is 9 (UP).
            # Is there any case where we are at x (x<15) and came from x-1, but next is DOWN?
            # No, because the cycle is deterministic. If we are in the ascending phase, next is ascending.
            # UNLESS we are at 15.
            # So if was_up and last_val != 15, then next is UP.
            print("UP")
            
    elif was_down:
        # The moon was decreasing.
        if last_val == 0:
            # Must be UP
            print("UP")
        elif last_val == 15:
            # Impossible to go down from 15 unless previous was 16, which is invalid.
            # So if was_down, last_val cannot be 15.
            print("DOWN") # Should not happen
        else:
            # If we are at x (x>0) and came from x+1, next is x-1 (DOWN).
            # Is there any case where we are at x (x>0) and came from x+1, but next is UP?
            # Only if x=0, but we handled that.
            # So if was_down and last_val != 0, then next is DOWN.
            print("DOWN")

solve()