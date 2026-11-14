import sys
import math

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

    passengers = []
    seats = []

    for r in range(R):
        for c in range(C):
            if grid[r][c] == 'X':
                passengers.append((r, c))
            elif grid[r][c] == 'L':
                seats.append((r, c))

    explosions = 0

    while passengers and seats:
        # Calculate distances for each passenger to each available seat
        passenger_best = {}  # passenger_idx -> (min_dist, seat_idx)
        seat_demand = {}     # seat_idx -> count of passengers targeting it as best

        for p_idx, (pr, pc) in enumerate(passengers):
            best_dist = float('inf')
            best_seat = -1
            for s_idx, (sr, sc) in enumerate(seats):
                d = math.sqrt((pr - sr)**2 + (pc - sc)**2)
                if d < best_dist:
                    best_dist = d
                    best_seat = s_idx
                # If equal distance, we don't update because we want the first one found?
                # Actually, the problem says: "If they are all equally close, they will all run to the seat"
                # This implies we need to group by distance.
                # Let's re-evaluate: We need to find the minimum distance for each passenger.
                # Then check if multiple passengers have the SAME minimum distance to the SAME seat.
                # But wait, the rule is: "If one of them is the closest, he or she will sit... If however they are all equally close, they will all run to the seat"
                # This phrasing is slightly ambiguous. Does "all equally close" mean:
                # 1. Multiple passengers have the same distance to a specific seat (collision on that seat)?
                # 2. Or does it mean a passenger has multiple seats at the same minimal distance?
                #
                # Re-reading: "If they spot more than one place, they always try the closest one first."
                # "If one of them is the closest, he or she will sit" -> implies if a passenger has a unique closest seat, they take it.
                # "If however they are all equally close, they will all run to the seat" -> This likely refers to the scenario where multiple passengers target the SAME seat and that seat is the closest for ALL of them (or at least tied for closest among their options).
                #
                # Let's look at the constraint: "Also, there will be no two 'L' characters such that they are both equally distant to some 'X'."
                # This constraint simplifies things greatly. It means for any passenger, if there are two seats at the same minimal distance, that situation won't happen for any pair of seats relative to a single passenger?
                # Wait, "no two 'L' characters such that they are both equally distant to some 'X'".
                # This means for any specific passenger X, all available seats have UNIQUE distances.
                # Therefore, every passenger has exactly ONE unique closest seat.
                #
                # So the logic simplifies to:
                # 1. For each passenger, find their unique closest seat.
                # 2. Count how many passengers want each seat.
                # 3. If a seat is wanted by exactly 1 passenger, that passenger sits (remove both).
                # 4. If a seat is wanted by >1 passengers, an explosion occurs (remove all those passengers and the seat).
                #
                # Is it possible for a passenger to have a tie? The constraint says "no two 'L' ... equally distant to some 'X'".
                # This strictly forbids ties for a single passenger. So every passenger has a unique closest seat.
                #
                # What if Passenger A wants Seat 1 (dist 5) and Passenger B wants Seat 1 (dist 5)?
                # Then Seat 1 is the closest for both. They collide. Explosion.
                # What if Passenger A wants Seat 1 (dist 5) and Passenger B wants Seat 2 (dist 5)?
                # No collision, they take their respective seats.
                #
                # So the algorithm is:
                # Map each passenger to their unique closest seat index.
                # Count frequencies of seat indices.
                # If count == 1: match (remove passenger, remove seat).
                # If count > 1: explosion (remove all involved passengers, remove the seat).
                # Note: If a seat is targeted by >1 passengers, ALL of them explode, even if one of them might have had a closer option?
                # No, because we established every passenger has a UNIQUE closest seat. So if they target a seat, it IS their closest.
                # If multiple target the same seat, they all have that same distance to it. Since distances are unique per passenger, they must be the same value.
                # So yes, if count > 1, explosion.

        # Build mapping: passenger_idx -> seat_idx
        p_to_s = {}
        for p_idx, (pr, pc) in enumerate(passengers):
            min_d = float('inf')
            best_s = -1
            for s_idx, (sr, sc) in enumerate(seats):
                d = math.sqrt((pr - sr)**2 + (pc - sc)**2)
                if d < min_d:
                    min_d = d
                    best_s = s_idx
            p_to_s[p_idx] = best_s

        # Count demands per seat
        seat_counts = {}
        for p_idx, s_idx in p_to_s.items():
            seat_counts[s_idx] = seat_counts.get(s_idx, 0) + 1

        # Process outcomes
        passengers_to_remove = set()
        seats_to_remove = set()

        for s_idx, count in seat_counts.items():
            if count == 1:
                # Find which passenger wants this seat
                for p_idx, target_s in p_to_s.items():
                    if target_s == s_idx:
                        passengers_to_remove.add(p_idx)
                        break
                # Seat is taken safely
            else:
                # Explosion
                explosions += 1
                # All passengers targeting this seat explode
                for p_idx, target_s in p_to_s.items():
                    if target_s == s_idx:
                        passengers_to_remove.add(p_idx)
                seats_to_remove.add(s_idx)

        # Update lists
        # We need to rebuild the lists to maintain consistency for next iteration
        # Also remove the exploded seats from the 'seats' list
        new_seats = []
        for i, s in enumerate(seats):
            if i not in seats_to_remove:
                new_seats.append(s)
        seats = new_seats

        new_passengers = []
        for i, p in enumerate(passengers):
            if i not in passengers_to_remove:
                new_passengers.append(p)
        passengers = new_passengers

    print(explosions)

if __name__ == "__main__":
    solve()