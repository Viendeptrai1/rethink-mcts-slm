import sys

def solve():
    input = sys.stdin.read().split()
    n = int(input[0])
    k = int(input[1])
    s = input[2]

    free_indices = [i for i, ch in enumerate(s) if ch == '0']
    total_needed = k + 1
    total_free = len(free_indices)

    if total_free < total_needed:
        return  # Should not happen based on problem guarantee

    best = float('inf')

    # We need to select a window of size total_needed from free_indices
    # Let the chosen indices be w[0], w[1], ..., w[m-1] where m = total_needed
    # We assign one of these to Farmer John such that max(j - i) is minimized.
    # Optimal strategy for a fixed window:
    # If we pick the j-th element in the window as Farmer John's room,
    # the farthest cow will be either the first (index 0) or the last (index m-1) in the window.
    # Distance = max(|w[0] - w[j]|, |w[m-1] - w[j]|)
    # We want to minimize this over j in [0, m-1].
    # The function f(j) = max(w[j] - w[0], w[m-1] - w[j]) is convex and minimized when w[j] is the midpoint.
    # So we check j around (0 + m-1) // 2.

    m = total_needed
    for i in range(total_free - m + 1):
        window = free_indices[i:i+m]
        left = window[0]
        right = window[-1]
        # Find j that minimizes max(w[j]-left, right-w[j])
        # This occurs when w[j] is closest to (left + right) / 2
        target = (left + right) / 2
        # We can just check the two candidates around target in the window
        # But since window is sorted, we can use bisect or linear scan for small m? 
        # m can be up to 100,000, so we need O(1) per window -> use index directly.
        # The optimal j in terms of value is the one where w[j] is closest to target.
        # We can find the insertion point of target in window.
        import bisect
        idx = bisect.bisect_left(window, target)
        # Check idx and idx-1 if they exist
        candidates = []
        if 0 <= idx < m:
            candidates.append(idx)
        if 0 <= idx - 1 < m:
            candidates.append(idx - 1)
        
        local_min = float('inf')
        for j in candidates:
            dist = max(window[j] - left, right - window[j])
            if dist < local_min:
                local_min = dist
        if local_min < best:
            best = local_min

    print(best)

if __name__ == "__main__":
    solve()