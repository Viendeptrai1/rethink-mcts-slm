import sys
import math

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    R = int(input_data[idx])
    C = int(input_data[idx+1])
    idx += 2
    
    grid = []
    for _ in range(R):
        grid.append(input_data[idx])
        idx += 1
    
    # Collect all 'X' positions
    passengers = []
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 'X':
                passengers.append((r, c))
    
    # Collect all 'L' positions
    seats = []
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 'L':
                seats.append((r, c))
    
    explosions = 0
    
    # We need to simulate the process:
    # While there are passengers who haven't sat and there are seats available:
    # 1. For each passenger, calculate distance to all available seats.
    # 2. Find the minimum distance among all (passenger, seat) pairs where seat is available.
    # 3. Check how many passengers have this exact minimum distance to their closest available seat.
    #    But the rule is: "If they are all equally close [to the SAME spot], they will all run to the seat".
    #    Actually, re-reading: "If however they are all equally close, they will all run to the seat".
    #    Context: "If one of them is the closest, he or she will sit... If however they are all equally close".
    #    This implies: Identify the specific seat that is the closest target.
    #    Let d_min be the minimum distance from any passenger to any available seat.
    #    Consider the set of (passenger, seat) pairs where dist(passenger, seat) == d_min.
    #    If there are multiple passengers targeting the SAME seat with distance d_min, AND that is the closest option for them?
    #    Let's refine the logic based on standard competitive programming interpretations of this specific problem (SPOJ TRAM).
    
    # Correct Logic Interpretation:
    # In each step:
    # 1. Calculate the distance from every passenger to every available seat.
    # 2. Find the global minimum distance 'd' among all valid (passenger, seat) pairs.
    # 3. Identify all seats 's' such that there exists at least one passenger 'p' where dist(p, s) == d.
    # 4. For a specific seat 's', count how many passengers have 's' as their closest seat AND dist(p, s) == d.
    #    Actually, simpler: 
    #    - Find all pairs (p, s) such that dist(p, s) is minimal for p among all available seats. Let this minimal distance for p be d_p.
    #    - Among all passengers, find the global minimum d_min = min(d_p for all p).
    #    - Consider the set of seats S_target that are closest to some passenger with distance d_min.
    #    - If a seat s in S_target is the unique closest seat for a passenger p (i.e., no other available seat is at distance d_min for p? No, Euclidean distances are unique per pair usually, but multiple passengers can be equidistant to one seat).
    #    - The explosion condition: Two or more passengers target the SAME seat, and that seat is at the minimal distance d_min for those passengers.
    #    - Wait, the problem says: "If they are all equally close, they will all run to the seat". This usually means:
    #      Find the set of candidates (passenger, seat) where dist(p, s) == d_min.
    #      Group these by seat.
    #      If a seat has >1 passenger in this group, EXPLOSION occurs. Those passengers are removed (destroyed), seat is destroyed (removed).
    #      If a seat has exactly 1 passenger in this group, that passenger sits (removed), seat taken (removed).
    #      What if a passenger has two seats at distance d_min? (Impossible by problem statement: "no two 'L' characters such that they are both equally distant to some 'X'").
    
    # So the algorithm per step:
    # 1. For each passenger, find the distance to the nearest available seat. Let this be min_dist[p].
    # 2. Find global_min = min(min_dist[p] for all remaining passengers).
    # 3. Identify all (passenger, seat) pairs where dist(p, seat) == global_min.
    # 4. Group these pairs by seat.
    # 5. For each seat in the groups:
    #    - If count == 1: Passenger sits. Remove passenger, remove seat.
    #    - If count > 1: Explosion. Remove all involved passengers, remove seat. Increment explosion count.
    #    - Note: If a seat has count > 1, ALL passengers targeting it explode. Even if one of them was "closest" in a general sense, the tie causes explosion.
    
    # Wait, re-read: "If one of them is the closest, he or she will sit". 
    # "Closest" implies strictly closest? Or just that among the group aiming for this seat, one is closer than the others? 
    # But the constraint says no two L are equidistant to an X. So for a specific passenger, distances to different seats are unique.
    # The ambiguity is: Can a passenger have two seats at the same distance? No.
    # Can multiple passengers have the same distance to the same seat? Yes.
    # The condition "If one of them is the closest" refers to the competition for a specific seat.
    # If Passenger A is 5m away, Passenger B is 5m away -> Tie -> Explosion.
    # If Passenger A is 5m away, Passenger B is 6m away -> A sits.
    # So we only care about the global minimum distance first.
    
    # Revised Step-by-Step Algorithm:
    # While there are passengers and seats:
    #   1. Compute distances from all passengers to all available seats.
    #   2. Find the absolute minimum distance 'd' among all valid (passenger, seat) pairs.
    #   3. Identify all seats that are at distance 'd' from at least one passenger.
    #   4. For each such seat, count how many passengers are at distance 'd' from it.
    #      (Note: A passenger cannot be at distance 'd' from two different seats because 'd' is the global minimum. If a passenger had another seat at 'd', it would still be 'd'. But the problem guarantees uniqueness of distances from one X to multiple Ls? "no two 'L' characters such that they are both equally distant to some 'X'". Yes, so each passenger has a unique closest seat. If dist(p, s1) == d and dist(p, s2) == d, then s1 == s2. So each passenger contributes to at most one seat in the 'd' layer).
    #   5. Process these seats:
    #      - If a seat has 1 passenger: Passenger sits, seat removed.
    #      - If a seat has >1 passengers: Explosion. All those passengers destroyed, seat removed. Count explosion.
    #   6. If no seats were processed (no passengers left or no seats left), break.
    
    # Wait, is it possible that a passenger's closest seat is NOT at the global minimum?
    # No. If a passenger's closest seat is at distance d_p, and there exists some other pair (p', s') with dist < d_p, then d_p is not the global minimum.
    # However, we only consider the global minimum distance 'd' to decide who moves first.
    # Why? Because "If one of them is the closest [to the seat], he or she will sit".
    # This implies the race happens for the closest available spots first.
    # Actually, the standard interpretation for this problem (SPOJ TRAM) is:
    # Always look at the minimum distance d between ANY passenger and ANY available seat.
    # Look at all pairs (p, s) with dist(p, s) == d.
    # If a seat s has multiple p's, explosion.
    # If a seat s has one p, that p sits.
    # Passengers whose closest seat is > d do not move yet.
    
    # Implementation:
    
    while passengers and seats:
        # Calculate distances
        # Map seat -> list of passengers at min distance d
        # Also need to ensure we only consider the GLOBAL minimum d
        
        # Step 1: Find global min distance
        min_d = float('inf')
        for p in passengers:
            for s in seats:
                d = math.sqrt((p[0]-s[0])**2 + (p[1]-s[1])**2)
                if d < min_d:
                    min_d = d
        
        # Step 2: Group pairs by seat for this min_d
        seat_to_passengers = {}
        
        # We need to handle floating point comparisons carefully. 
        # Since inputs are integers, squared distances are integers. 
        # Let's work with squared distances to avoid precision issues.
        # min_d_sq = min((p[0]-s[0])**2 + (p[1]-s[1])**2)
        
        min_d_sq = float('inf')
        for p in passengers:
            for s in seats:
                d_sq = (p[0]-s[0])**2 + (p[1]-s[1])**2
                if d_sq < min_d_sq:
                    min_d_sq = d_sq
        
        seat_to_passengers = {}
        
        for p in passengers:
            for s in seats:
                d_sq = (p[0]-s[0])**2 + (p[1]-s[1])**2
                if d_sq == min_d_sq:
                    if s not in seat_to_passengers:
                        seat_to_passengers[s] = []
                    seat_to_passengers[s].append(p)
        
        # Process the collisions
        made_change = False
        for s in list(seat_to_passengers.keys()):
            p_list = seat_to_passengers[s]
            count = len(p_list)
            if count == 1:
                # Passenger sits
                idx_p = passengers.index(p_list[0])
                passengers.pop(idx_p)
                seats.remove(s)
                made_change = True
            elif count > 1:
                # Explosion
                explosions += 1
                # Remove all involved passengers
                for p in p_list:
                    if p in passengers:
                        passengers.remove(p)
                # Remove seat
                seats.remove(s)
                made_change = True
        
        if not made_change:
            # Should not happen if passengers and seats are not empty and logic is correct
            break
    
    print(explosions)

if __name__ == "__main__":
    solve()