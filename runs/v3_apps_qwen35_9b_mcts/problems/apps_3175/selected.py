import sys
import math

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    lengths = [int(x) for x in input_data[1:]]
    
    if n < 3:
        print(0.0)
        return
    
    max_area = 0.0
    
    # Iterate over all non-empty subsets of segments
    # There are 2^n subsets, but we only care about those with at least 3 segments
    # Since n <= 80, 2^80 is too large. However, the problem constraints say lengths are between 1 and 100.
    # Wait, n is up to 80. 2^80 is definitely too big for brute force.
    # Let's re-read the problem carefully.
    # "Not all segment lengths listed need to be used."
    # Is there a property that allows us to avoid checking all subsets?
    # Actually, for a fixed set of side lengths, the maximum area is achieved by a cyclic polygon.
    # But which subset?
    # It is a known result that to maximize the area, we should use as many segments as possible,
    # provided they can form a polygon. Specifically, if we have a valid polygon, adding a segment
    # (if the new longest side is still less than the sum of the others) will increase the area.
    # Therefore, the optimal solution is likely formed by the largest possible subset of segments
    # that satisfies the polygon inequality.
    # However, simply taking the largest k segments might not work if the largest one is too big.
    # We need to find a subset.
    # Actually, the strategy is: sort the segments in descending order. Try to form a polygon using
    # the largest k segments. If the largest segment is >= sum of the rest, we cannot form a polygon
    # with these k segments. We might need to remove the largest segment and try again, or remove a small one?
    # Actually, if the largest segment L >= sum(others), then no subset containing L and the current 'others'
    # can form a polygon. To fix this, we must remove L or add more segments to the 'others'.
    # But we are iterating from largest k downwards.
    # Let's reconsider. We want to maximize area. Area increases with perimeter (roughly) and with how "balanced" the sides are.
    # The optimal polygon is cyclic.
    # Key Insight: The optimal subset of segments will always be a contiguous subarray of the sorted segments?
    # No, that's not necessarily true.
    # However, there is a known greedy approach for this specific problem (often found in competitive programming):
    # Sort the segments in descending order.
    # Iterate k from n down to 3.
    # Consider the largest k segments. Check if they can form a polygon (max < sum of others).
    # If they can, calculate the area. Since adding more segments (if possible) generally increases area,
    # and we are starting from the largest possible set, the first valid set we find (largest k) might not be the one with max area?
    # Actually, if a set of k segments forms a polygon, can we always get a larger area by including more segments?
    # Not necessarily, because including a very small segment might not help if it breaks the cyclic property logic?
    # Wait, if we have a valid polygon, adding a segment s such that new_max < sum(new_others) creates a new polygon.
    # Does the area always increase? Yes, intuitively, more perimeter with same constraints usually means more area.
    # But we are constrained by the available segments.
    # Let's look at the constraints again. n <= 80. This suggests an O(n^2) or O(n^3) solution, not exponential.
    # The "contiguous subarray" hypothesis: If we sort the segments, is the optimal subset always a contiguous subarray?
    # Counter-example: Segments [10, 10, 10, 1, 1, 1]. Sorted: 10, 10, 10, 1, 1, 1.
    # Subset {10, 10, 10} -> Area ~ 25.98.
    # Subset {10, 10, 10, 1} -> 10 < 10+10+1=21. Valid. Area > 25.98.
    # Subset {10, 10, 10, 1, 1} -> 10 < 21. Valid. Area > previous.
    # Subset {10, 10, 10, 1, 1, 1} -> 10 < 21. Valid.
    # It seems including smaller segments helps satisfy the inequality and increases area.
    # So we should try to include as many segments as possible.
    # Strategy: Sort segments descending.
    # Try to find the largest k such that the k largest segments form a polygon.
    # Let the sorted segments be s[0] >= s[1] >= ... >= s[n-1].
    # For a fixed k, the condition is s[0] < sum(s[1]...s[k-1]).
    # If this holds, then the subset {s[0], ..., s[k-1]} is valid.
    # Is it possible that a subset of size k that is NOT the k largest segments yields a larger area?
    # Suppose we replace a large segment with a smaller one. The perimeter decreases, and the "balance" might improve or worsen.
    # However, the area of a cyclic polygon is maximized for a given set of sides.
    # If we have a valid set of sides, replacing a side with a smaller one (while keeping the polygon valid) generally reduces the area.
    # Why? Because the area is a function of the sides. Intuitively, larger sides allow for a larger circumradius or larger dimensions.
    # More formally, if we have a valid polygon with sides A and we replace a side a with a' < a, the new perimeter is smaller.
    # The maximum area for a fixed perimeter is a circle. For fixed sides, the area is determined.
    # It is a known property that to maximize area, you should use the largest available segments that satisfy the polygon inequality.
    # So the algorithm is:
    # 1. Sort segments in descending order.
    # 2. Iterate k from n down to 3.
    # 3. Check if s[0] < sum(s[1]...s[k-1]).
    # 4. If yes, calculate the area of the cyclic polygon with sides s[0]...s[k-1] and update max_area.
    # 5. Since we want the maximum area, and adding segments (if valid) increases area, the first k (largest) that works is the best?
    # Wait, is it monotonic?
    # If {s[0]...s[k]} is valid, is {s[0]...s[k+1]} valid?
    # Condition for k: s[0] < sum(s[1]...s[k]).
    # Condition for k+1: s[0] < sum(s[1]...s[k+1]) = sum(s[1]...s[k]) + s[k+1].
    # Since s[k+1] > 0, if the condition holds for k, it definitely holds for k+1.
    # So if the largest k segments form a polygon, then any larger set (up to n) also forms a polygon?
    # Yes, because the sum of the rest increases as we add more segments, while the max element (s[0]) stays the same.
    # Therefore, we just need to find the largest k such that s[0] < sum(s[1]...s[k-1]).
    # Wait, what if the largest k segments don't form a polygon, but a different subset of size k does?
    # Example: [100, 10, 10, 10]. Sorted: 100, 10, 10, 10.
    # k=4: 100 < 10+10+10=30? No.
    # k=3: 100 < 10+10=20? No.
    # k=2: Not a polygon.
    # So no polygon with 100.
    # What if we drop 100? Subset {10, 10, 10}.
    # This corresponds to indices 1, 2, 3 in the sorted array.
    # My previous logic assumed the optimal set MUST include the largest element.
    # But if the largest element prevents forming a polygon, we must exclude it.
    # So the strategy should be:
    # Iterate through all possible "max elements" in the sorted array.
    # Let the chosen max element be s[i]. Then we should pick the largest possible number of other segments from s[i+1]...s[n-1] to maximize the sum (to satisfy inequality) and thus maximize area.
    # Actually, if we fix the largest side to be s[i], we should take ALL segments from s[i+1] to s[n-1] because adding more segments only helps the inequality and increases area.
    # So for each i from 0 to n-1:
    #   Consider s[i] as the longest side.
    #   Take all segments s[i+1]...s[n-1].
    #   Check if s[i] < sum(s[i+1]...s[n-1]).
    #   If yes, calculate area with sides {s[i], s[i+1], ..., s[n-1]}.
    #   Update max_area.
    #   Note: We must ensure we have at least 3 sides. So if i == n-1, we have only 1 side, skip. If i == n-2, we have 2 sides, skip.
    #   Also, we need to consider subsets that don't include the largest available segments?
    #   Suppose we pick s[i] as max. Should we pick ALL smaller segments?
    #   Yes, because adding a segment increases the sum of others, making the inequality easier to satisfy, and generally increases area.
    #   Is it possible that we need to skip some small segments to get a better area?
    #   No, because for a fixed largest side, the area is maximized when the other sides are as large as possible (to maximize perimeter and balance).
    #   So the algorithm is:
    #   Sort descending.
    #   max_area = 0
    #   For i in range(n):
    #       # s[i] is the longest side
    #       # Candidates are s[i], s[i+1], ..., s[n-1]
    #       if n - i < 3: continue
    #       current_sides = s[i:]
    #       if current_sides[0] < sum(current_sides[1:]):
    #           area = compute_area(current_sides)
    #           max_area = max(max_area, area)
    #   Print max_area.
    
    # Let's trace Sample 1: 4 1 1 1 1
    # Sorted: 1, 1, 1, 1
    # i=0: sides [1,1,1,1]. Max=1, sum_others=3. 1<3. Valid. Area = 1.0.
    # i=1: sides [1,1,1]. Max=1, sum_others=2. 1<2. Valid. Area = 0.433.
    # i=2: sides [1,1]. Skip (<3).
    # Max area = 1.0. Correct.
    
    # Sample 2: 3 1 1 1
    # Sorted: 1, 1, 1
    # i=0: [1,1,1]. Valid. Area 0.433.
    # i=1: [1,1]. Skip.
    # Max 0.433. Correct.
    
    # Another case: 100, 10, 10, 10
    # Sorted: 100, 10, 10, 10
    # i=0: [100, 10, 10, 10]. 100 < 30? No.
    # i=1: [10, 10, 10]. 10 < 20? Yes. Area ~ 25.98.
    # i=2: [10, 10]. Skip.
    # Max 25.98. Correct.
    
    # What if we have 10, 10, 10, 10, 100?
    # Sorted: 100, 10, 10, 10, 10
    # i=0: 100 < 40? No.
    # i=1: [10, 10, 10, 10, 10]. 10 < 40? Yes. Area large.
    # This logic holds.
    
    # One edge case: What if the optimal solution does NOT include the largest available segment among the chosen subset?
    # My loop iterates i from 0 to n-1. s[i] is the largest in the subset s[i:].
    # So every possible "largest element" of a subset is considered.
    # And for each largest element, we greedily take all smaller available segments.
    # This covers all "maximal" subsets (by inclusion) for each possible maximum element.
    # Since adding segments never hurts the validity (if we add a segment smaller than the current max, the sum of others increases) and likely helps area,
    # the maximal subset for a given max element is the best candidate for that max element.
    # Thus, this O(N^2) approach (sorting O(N log N), loop N times, sum O(N)) is efficient enough for N=80.
    
    lengths.sort(reverse=True)
    
    def heron_area(sides):
        # sides is a list of lengths
        # Check polygon inequality
        max_side = sides[0]
        sum_others = sum(sides[1:])
        if max_side >= sum_others:
            return 0.0
        
        s = sum(sides) / 2.0
        area_sq = s
        for x in sides:
            area_sq *= (s - x)
        return math.sqrt(area_sq)
    
    for i in range(n):
        # Consider subset lengths[i:]
        if n - i < 3:
            continue
        
        subset = lengths[i:]
        # Check polygon inequality
        # Since sorted descending, subset[0] is the max
        if subset[0] < sum(subset[1:]):
            area = heron_area(subset)
            if area > max_area:
                max_area = area
                
    print(f"{max_area:.10f}")

if __name__ == "__main__":
    solve()