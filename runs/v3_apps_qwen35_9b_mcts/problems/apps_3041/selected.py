import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    # Current ticket state: [A, B] interval, expiration time
    # Initially no ticket: we can represent this as A=0, B=0, exp=0
    # But logically, if no ticket, we must buy one.
    # Let's track the current valid interval [cur_A, cur_B] and expiration time cur_exp.
    # If no ticket is active, we can set cur_A, cur_B to something that forces a buy, 
    # but simpler: just use a flag or check if cur_exp <= current_time.
    
    cur_A = 0
    cur_B = 0
    cur_exp = 0
    total_coupons = 0
    
    # Previous trip end time is not needed because a ticket is valid for 10000 seconds from purchase.
    # However, the problem says "valid for exactly 10000 seconds". 
    # When we buy a ticket at time T_start, it expires at T_start + 10000.
    # The ticket covers any trip starting at time T if T <= cur_exp.
    # The ticket covers a trip from zone Z_start to Z_end if both Z_start and Z_end are in [cur_A, cur_B].
    # Note: The problem says "starts and ends in zones in the interval". 
    # Since we are given the destination zone and start is previous location, we need to track current location.
    # Wait, the problem says: "For each trip, you will be given the zone Johan travels to".
    # "Initially, Johan is located in zone 0".
    # So for trip i: start_zone = current_location, end_zone = Z_i.
    # After trip i, current_location becomes Z_i.
    
    current_location = 0
    
    for _ in range(N):
        Z = int(next(iterator))
        T = int(next(iterator))
        
        # Check if current ticket is still valid at time T
        # Valid if: T <= cur_exp AND current_location and Z are both in [cur_A, cur_B]
        can_use_current = False
        if cur_exp >= T:
            if cur_A <= current_location <= cur_B and cur_A <= Z <= cur_B:
                can_use_current = True
        
        if can_use_current:
            # We can use the current ticket. No cost.
            # Update location
            current_location = Z
        else:
            # Must buy a new ticket.
            # We need to cover the trip from current_location to Z.
            # The ticket must be valid at time T.
            # Cost = 2 + |A - B|.
            # To minimize cost, we want to minimize |A - B| such that [A, B] covers both current_location and Z.
            # The minimal interval covering two points x and y is [min(x,y), max(x,y)].
            # Let A_new = min(current_location, Z)
            # Let B_new = max(current_location, Z)
            # Cost = 2 + (B_new - A_new)
            
            A_new = min(current_location, Z)
            B_new = max(current_location, Z)
            cost = 2 + (B_new - A_new)
            total_coupons += cost
            
            # Update ticket state
            cur_A = A_new
            cur_B = B_new
            cur_exp = T + 10000
            
            # Update location
            current_location = Z

    print(total_coupons)

if __name__ == "__main__":
    solve()