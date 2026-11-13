import sys
import math
import heapq

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        R = int(next(iterator))
        C = int(next(iterator))
    except StopIteration:
        return

    grid = []
    for _ in range(R):
        grid.append(next(iterator))

    # Collect all 'X' positions
    rude_passengers = []
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 'X':
                rude_passengers.append((r, c))

    # Collect all 'L' positions
    seats = []
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 'L':
                seats.append((r, c))

    # We need to simulate the process.
    # The problem states:
    # 1. Rude passengers look for the closest seat.
    # 2. If multiple seats are equally close, they all run to it -> EXPLOSION.
    # 3. If a seat is taken by the closest person(s), others look at the next closest.
    # 4. The problem guarantees: "no two 'L' characters such that they are both equally distant to some 'X'".
    #    This simplifies things: for any specific 'X', there is a unique closest seat.
    #    However, an explosion happens if multiple 'X's have the SAME closest seat.
    #
    # Wait, let's re-read carefully: "If however they are all equally close, they will all run to the seat".
    # This implies if Passenger A and Passenger B both have Seat S as their unique closest seat, they collide.
    # What if Passenger A has Seat S1 (dist 5) and Passenger B has Seat S1 (dist 5)? Collision.
    # What if Passenger A has Seat S1 (dist 5) and Passenger B has Seat S2 (dist 5)?
    #    - A's closest is S1. B's closest is S2. No collision on S1.
    #    - But what if S1 and S2 are the same seat? Then collision.
    #
    # The guarantee "no two 'L' characters such that they are both equally distant to some 'X'" means:
    # For a fixed X, the distances to all seats are distinct. So X has a unique closest seat.
    #
    # So the algorithm is:
    # 1. For each 'X', find the distance to every 'L'.
    # 2. Identify the minimum distance for that 'X'.
    # 3. Identify which 'L' is the closest for that 'X'.
    # 4. Count how many 'X's target the same 'L' as their closest seat.
    #    - If count == 1: That 'X' sits there. The seat is removed.
    #    - If count > 1: EXPLOSION. All those 'X's are destroyed (or removed), and that seat is destroyed (removed).
    #      The remaining 'X's (if any) still need seats. They will re-evaluate their closest available seat.
    #
    # Wait, the problem says: "If one of them is the closest, he or she will sit, and others won't even attempt...".
    # This implies a tie-breaking rule based on who is "closest". But the guarantee says distances from a single X to seats are unique.
    # It does NOT say distances from different X's to a seat are unique.
    #
    # Re-reading: "If however they are all equally close, they will all run to the seat".
    # "Equally close" refers to the distance from the passengers to the seat.
    # So if X1 and X2 both have distance D to Seat S, and D is the minimum for both, they collide.
    #
    # Scenario:
    # X1 -> S (dist 5)
    # X2 -> S (dist 5)
    # Both want S. Collision.
    #
    # Scenario:
    # X1 -> S1 (dist 5)
    # X2 -> S1 (dist 6)
    # X1 wants S1. X2's closest might be S2 (dist 4).
    # X1 takes S1. X2 takes S2. No collision.
    #
    # Scenario:
    # X1 -> S1 (dist 5)
    # X2 -> S1 (dist 5)
    # X3 -> S2 (dist 5)
    # X1 and X2 collide on S1. S1 is gone. X1 and X2 are gone.
    # X3 takes S2.
    #
    # So the simulation step:
    # 1. Calculate for each remaining 'X', the closest available 'L' and its distance.
    #    (Note: The guarantee ensures that for a given X, the closest L is unique among ALL Ls initially.
    #     Does it hold for remaining Ls? Yes, because we just remove one L. The set of distances shrinks,
    #     but the minimum is still unique unless the unique minimum was removed. If the unique minimum is removed,
    #     the new minimum is also unique by the same logic applied to the subset).
    # 2. Group 'X's by their target 'L'.
    # 3. For each target 'L':
    #    - If number of 'X's targeting it is 1:
    #        - That 'X' sits. Remove 'X' and 'L'.
    #    - If number of 'X's targeting it is > 1:
    #        - EXPLOSION count += 1.
    #        - Remove all those 'X's and the 'L'.
    # 4. Repeat until no 'X's or no 'L's remain.

    # Let's implement this simulation.

    # Store available seats in a set for O(1) lookup and removal
    available_seats = set(seats)
    # Store available passengers
    available_passengers = set(rude_passengers)

    explosions = 0

    while available_passengers and available_seats:
        # For each passenger, find the closest available seat
        passenger_targets = {} # seat -> list of passengers

        for px, py in available_passengers:
            min_dist = float('inf')
            target_seat = None
            
            # Find closest available seat
            for sx, sy in available_seats:
                d = math.sqrt((px - sx)**2 + (py - sy)**2)
                if d < min_dist:
                    min_dist = d
                    target_seat = (sx, sy)
            
            # By problem statement, target_seat is unique for this passenger
            if target_seat not in passenger_targets:
                passenger_targets[target_seat] = []
            passenger_targets[target_seat].append((px, py))

        # Process targets
        seats_to_remove = set()
        passengers_to_remove = set()

        for seat, p_list in passenger_targets.items():
            if len(p_list) == 1:
                # One person sits
                px, py = p_list[0]
                seats_to_remove.add(seat)
                passengers_to_remove.add((px, py))
            else:
                # Explosion
                explosions += 1
                for p in p_list:
                    passengers_to_remove.add(p)
                seats_to_remove.add(seat)

        # Update state
        for s in seats_to_remove:
            available_seats.discard(s)
        for p in passengers_to_remove:
            available_passengers.discard(p)

    print(explosions)

if __name__ == '__main__':
    solve()