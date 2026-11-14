import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    n = int(next(iterator))
    k = int(next(iterator))
    m = int(next(iterator))

    a = []
    for _ in range(n):
        a.append(int(next(iterator)))

    a.sort(reverse=True)

    # Calculate prefix sums for O(1) sum queries of the top i elements
    # prefix_sum[i] = sum of the first i elements (largest i)
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + a[i]

    max_avg = 0.0

    # Try removing i elements, where i ranges from 0 to min(n-1, m)
    # We cannot remove all elements because we need at least 2 to perform a removal operation?
    # Actually, the problem says "if there are at least two". 
    # If we have 1 element, we can only increase it.
    # However, the strategy of removing smallest elements implies we stop removing when we have 1 left or m operations used.
    # Let's iterate on the number of elements remaining: rem_count from 1 to n.
    # But we can only remove up to m elements. So rem_count >= n - m.
    # Also, we can't remove n-1 elements if n=1? If n=1, we can't remove anything.
    
    # Let's iterate on the number of elements we KEEP. Let this be 'keep'.
    # keep can range from max(1, n - m) to n.
    # Why max(1, n-m)? Because we can remove at most m elements.
    # If n - m < 1, we can keep at least 1 element.
    
    min_keep = max(1, n - m)
    max_keep = n

    for keep in range(min_keep, max_keep + 1):
        # Number of removals
        removed_count = n - keep
        
        # Check if this number of removals is valid (<= m)
        if removed_count > m:
            continue

        # Current sum of the 'keep' largest elements
        current_sum = prefix_sum[keep]
        
        # Remaining operations after removals
        ops_left = m - removed_count
        
        # We can distribute ops_left among the 'keep' elements.
        # Each element can receive at most k.
        # Total capacity to increase = keep * k
        total_capacity = keep * k
        
        if ops_left >= total_capacity:
            # We can increase every element by k
            final_sum = current_sum + total_capacity
        else:
            # We can only increase by ops_left
            final_sum = current_sum + ops_left
        
        # Calculate average
        avg = final_sum / keep
        if avg > max_avg:
            max_avg = avg

    print(f"{max_avg:.20f}")

if __name__ == "__main__":
    solve()