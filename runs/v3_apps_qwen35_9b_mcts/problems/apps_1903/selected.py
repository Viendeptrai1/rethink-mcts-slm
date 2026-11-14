import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    try:
        n = int(next(iterator))
        m = int(next(iterator))
        d = int(next(iterator))
    except StopIteration:
        return

    physics = []
    for _ in range(n):
        c = int(next(iterator))
        w = int(next(iterator))
        physics.append((c, w))

    informatics = []
    for _ in range(m):
        c = int(next(iterator))
        w = int(next(iterator))
        informatics.append((c, w))

    # Sort Physics: significance descending, then width ascending
    physics.sort(key=lambda x: (-x[0], x[1]))
    # Sort Informatics: significance descending, then width ascending
    informatics.sort(key=lambda x: (-x[0], x[1]))

    # Precompute prefix sums for significance and width
    phys_sig = [0] * (n + 1)
    phys_w = [0] * (n + 1)
    for i in range(n):
        phys_sig[i+1] = phys_sig[i] + physics[i][0]
        phys_w[i+1] = phys_w[i] + physics[i][1]

    inf_sig = [0] * (m + 1)
    inf_w = [0] * (m + 1)
    for i in range(m):
        inf_sig[i+1] = inf_sig[i] + informatics[i][0]
        inf_w[i+1] = inf_w[i] + informatics[i][1]

    max_significance = 0

    # Iterate over the number of Physics cups to take (from 1 to n)
    for i in range(1, n + 1):
        current_phys_w = phys_w[i]
        current_phys_sig = phys_sig[i]

        if current_phys_w > d:
            # If the smallest width set of Physics cups (which is the top i by sig) exceeds d,
            # then any larger set will also exceed d. Since we are iterating i from 1 upwards,
            # and widths are positive, once we exceed d, we can stop? 
            # Actually, widths are positive, so phys_w[i] is strictly increasing.
            # So if phys_w[i] > d, we can break.
            break

        remaining_width = d - current_phys_w

        # We need at least 1 Informatics cup.
        # Find the maximum j such that inf_w[j] <= remaining_width.
        # We can use binary search (bisect_right on a list of widths) or a two-pointer approach.
        # Since i increases, remaining_width decreases, so the optimal j will decrease or stay same.
        # However, since we break early for Physics, a simple binary search for each i is O(N log M),
        # which is efficient enough for N, M <= 100,000.
        
        # Binary search for the largest j in [1, m] such that inf_w[j] <= remaining_width
        low = 1
        high = m
        best_j = 0
        
        while low <= high:
            mid = (low + high) // 2
            if inf_w[mid] <= remaining_width:
                best_j = mid
                low = mid + 1
            else:
                high = mid - 1
        
        if best_j >= 1:
            total_sig = current_phys_sig + inf_sig[best_j]
            if total_sig > max_significance:
                max_significance = total_sig

    print(max_significance)

if __name__ == '__main__':
    solve()