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

    # Sort both lists by significance descending
    physics.sort(key=lambda x: x[0], reverse=True)
    informatics.sort(key=lambda x: x[0], reverse=True)

    # Precompute suffix sums for significance and suffix sums for width for Physics
    # phys_sig[i] = sum of significances from index i to n-1
    # phys_w[i] = sum of widths from index i to n-1
    phys_sig = [0] * (n + 1)
    phys_w = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        phys_sig[i] = phys_sig[i + 1] + physics[i][0]
        phys_w[i] = phys_w[i + 1] + physics[i][1]

    # Precompute prefix sums for significance and prefix sums for width for Informatics
    # inf_sig[i] = sum of significances from index 0 to i-1 (first i items)
    # inf_w[i] = sum of widths from index 0 to i-1 (first i items)
    inf_sig = [0] * (m + 1)
    inf_w = [0] * (m + 1)
    for i in range(m):
        inf_sig[i + 1] = inf_sig[i] + informatics[i][0]
        inf_w[i + 1] = inf_w[i] + informatics[i][1]

    max_total_significance = 0

    # Try all possible numbers of Informatics cups to take (k from 1 to m)
    for k in range(1, m + 1):
        # Minimum width required for k Informatics cups (must be the top k)
        w_inf = inf_w[k]
        if w_inf > d:
            break  # Too wide, since we sorted by significance, taking more will only increase width

        sum_sig_inf = inf_sig[k]
        remaining_width = d - w_inf
        if remaining_width < 0:
            continue

        # We need to take at least 1 Physics cup (top i)
        # Iterate i from 1 to n
        # Optimization: Since we want to maximize, and width constraint is tight,
        # we can break early if width exceeds.
        # Also, we can stop if sum_sig_inf is already huge and remaining width is 0? 
        # No, we need to check all valid i.
        
        # To optimize, we can iterate i starting from 1 upwards.
        # As i increases, width increases and significance increases.
        # We stop when width exceeds remaining_width.
        
        current_w_phys = 0
        current_sig_phys = 0
        
        # We can iterate i from 1 to n
        for i in range(1, n + 1):
            c_i, w_i = physics[i-1]
            current_w_phys += w_i
            current_sig_phys += c_i
            
            if current_w_phys > remaining_width:
                break
            
            total_sig = sum_sig_inf + current_sig_phys
            if total_sig > max_total_significance:
                max_total_significance = total_sig

    print(max_total_significance)

if __name__ == "__main__":
    solve()