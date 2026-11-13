import sys
import math

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    segments = [int(x) for x in input_data[1:n+1]]

    # Sort segments in descending order to easily pick the largest k
    segments.sort(reverse=True)

    # Try all possible numbers of segments k from 3 to n
    # For a polygon to exist with k sides, the longest side must be less than the sum of the others.
    # To maximize area, we should pick the k largest segments.
    # If the condition is not met, we can't form a polygon with these k segments.
    
    max_area = 0.0

    # Precompute prefix sums for efficiency if needed, but n is small (<=80)
    # So slicing and summing is fine.

    for k in range(3, n + 1):
        # Take the k largest segments
        current_segments = segments[:k]
        
        # Check polygon inequality: longest < sum of others
        longest = current_segments[0]
        others_sum = sum(current_segments) - longest
        
        if longest >= others_sum:
            # Cannot form a polygon with these k segments (and since we picked largest, 
            # removing smaller ones won't help satisfy the inequality for the longest side)
            # Actually, if the largest of k fails, we might need to try fewer segments?
            # No, if the largest of k is >= sum of rest, removing any segment from 'rest' makes the gap worse.
            # Removing the largest itself? We handle that by iterating k.
            # But wait, if we have [10, 1, 1, 1], k=4: 10 >= 3 -> fail.
            # k=3: [10, 1, 1] -> 10 >= 2 -> fail.
            # k=3: [1, 1, 1] -> 1 < 2 -> success.
            # Our loop iterates k from 3 to n. Since segments are sorted descending,
            # segments[:k] always contains the largest k.
            # If segments[:k] fails the inequality, it means the largest element in that set 
            # is too big. Removing the largest element (by reducing k) might help.
            # However, we are iterating k upwards. We should check all valid k.
            # The condition "if longest >= others_sum" means we skip this k.
            continue

        # Calculate area using Brahmagupta's formula generalization (Parameshvara's formula)
        # For a cyclic polygon with sides a, b, c, d, ... the maximum area is achieved when it is cyclic.
        # Area = sqrt((s-a)(s-b)(s-c)...s) where s = perimeter / 2.
        
        s = sum(current_segments) / 2.0
        area_sq = 1.0
        possible = True
        
        for length in current_segments:
            val = s - length
            if val <= 0:
                possible = False
                break
            area_sq *= val
        
        if possible:
            area = math.sqrt(area_sq)
            if area > max_area:
                max_area = area

    print(f"{max_area:.9f}")

if __name__ == "__main__":
    solve()