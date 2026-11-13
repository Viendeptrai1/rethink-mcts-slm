import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    a = [int(input_data[i + 1]) for i in range(n)]

    # Try erasing every possible contiguous subsegment of length k from 1 to n-1
    # We want the maximum k such that the remaining elements uniquely determine the erased ones.
    # The condition for unique restoration:
    # 1. If we erase a segment from index i to j (inclusive, 0-based), the left neighbor is a[i-1] (if i>0) and right is a[j+1] (if j<n-1).
    # 2. The number of integers strictly between left and right is (right - left - 1).
    # 3. The number of erased elements is (j - i + 1).
    # 4. For uniqueness, we must have (number of gaps) == (number of erased elements).
    #    i.e., (a[j+1] - a[i-1] - 1) == (j - i + 1)
    #    Also, we need to handle boundary cases:
    #    - If left boundary doesn't exist (i==0), then the first erased element must be >= 1.
    #      The max possible value for the first element after erasure is determined by the right boundary.
    #      Actually, simpler logic:
    #      Let L = a[i-1] if i>0 else 0 (conceptually, but range starts at 1)
    #      Let R = a[j+1] if j<n-1 else 1001 (conceptually, max is 1000)
    #      Wait, the bounds are fixed: [1, 1000].
    #      If we erase from index i to j:
    #      Left bound value: prev = a[i-1] if i > 0 else 0
    #      Right bound value: next = a[j+1] if j < n-1 else 1001
    #      The gap between prev and next is (next - prev - 1).
    #      The number of erased elements is count = j - i + 1.
    #      If prev == 0, the values must be in [1, next-1]. Count of available slots = next - 1.
    #        We need exactly count numbers. So count == next - 1.
    #      If next == 1001, the values must be in [prev+1, 1000]. Count of available slots = 1000 - prev.
    #        We need count == 1000 - prev.
    #      If both exist (prev > 0 and next < 1001), then count == next - prev - 1.
    
    # Let's unify:
    # effective_prev = a[i-1] if i>0 else 0
    # effective_next = a[j+1] if j<n-1 else 1001
    # num_available = effective_next - effective_prev - 1
    # num_erased = j - i + 1
    # Check if num_available == num_erased

    max_erased = 0
    possible = False

    for i in range(n):
        for j in range(i, n):
            # Segment to erase: indices i to j
            count_erased = j - i + 1
            
            prev_val = a[i-1] if i > 0 else 0
            next_val = a[j+1] if j < n - 1 else 1001
            
            # Calculate how many integers are strictly between prev_val and next_val
            # But we must respect the global bounds [1, 1000] which are already encoded by setting 0 and 1001.
            # The number of integers x such that prev_val < x < next_val is exactly (next_val - prev_val - 1).
            # Since prev_val is 0 or a real value >= 1, and next_val is 1001 or a real value <= 1000.
            # Example: prev=1, next=3 -> integers: 2. Count = 3-1-1 = 1. Correct.
            # Example: prev=0, next=3 -> integers: 1, 2. Count = 3-0-1 = 2. Correct.
            # Example: prev=1, next=1001 -> integers: 2..1000. Count = 1001-1-1 = 999. Correct.
            
            num_slots = next_val - prev_val - 1
            
            if num_slots == count_erased:
                if count_erased > max_erased:
                    max_erased = count_erased
                possible = True

    # If no segment can be erased, output 0.
    # Note: The loops cover all segments. If max_erased remains 0, it means either n=1 (loop doesn't run effectively for length>=1) or no valid segment found.
    # Actually if n=1, loops: i=0, j=0. count=1. prev=0, next=1001. slots=1000. 1000!=1. max_erased=0. Correct.
    print(max_erased)

if __name__ == "__main__":
    solve()