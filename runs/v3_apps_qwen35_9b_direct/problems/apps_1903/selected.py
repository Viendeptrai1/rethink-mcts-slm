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
    
    # Precompute prefix sums for significance and width
    # pref_phys[i] = sum of widths of first i cups (0 to i-1)
    # sum_phys[i] = sum of significances of first i cups
    pref_phys = [0] * (n + 1)
    sum_phys = [0] * (n + 1)
    for i in range(n):
        pref_phys[i+1] = pref_phys[i] + physics[i][1]
        sum_phys[i+1] = sum_phys[i] + physics[i][0]
        
    pref_inf = [0] * (m + 1)
    sum_inf = [0] * (m + 1)
    for i in range(m):
        pref_inf[i+1] = pref_inf[i] + informatics[i][1]
        sum_inf[i+1] = sum_inf[i] + informatics[i][0]
        
    max_significance = 0
    
    # Try taking k cups from Physics (k from 1 to n)
    # Then try taking j cups from Informatics (j from 1 to m)
    # Optimization: For a fixed k, we need the smallest j such that total width <= d.
    # Since widths are positive, as k increases, the remaining width decreases, so j must decrease or stay same.
    # We can iterate k and find the max valid j using binary search or two pointers.
    
    # Let's use two pointers approach.
    # Start with k=1 (min physics cups), find max j.
    # As k increases, remaining width decreases, so max j can only decrease.
    
    # Initial state: k=1
    # Find max j such that pref_phys[1] + pref_inf[j] <= d
    
    # We'll iterate k from 1 to n
    # For each k, we want max j in [1, m] such that pref_phys[k] + pref_inf[j] <= d
    
    # Start j at m (or the max possible for k=1)
    # Actually, let's start j at m and decrease it as k increases.
    
    # First, find the max j for k=1
    current_k = 1
    current_w_phys = pref_phys[current_k]
    
    # Find max j for current_k
    # We can start j from m and go down until condition met
    # But to be efficient, let's just start j at m and decrement
    
    # However, for k=1, j could be large. Let's find the upper bound for j initially.
    # If pref_phys[1] > d, then no solution for any k >= 1 (since width only increases)
    if current_w_phys > d:
        print(0)
        return

    # Start j at m
    j = m
    # Ensure j is valid for k=1
    while j >= 1 and (pref_phys[current_k] + pref_inf[j] > d):
        j -= 1
    
    # If even j=0 (meaning no informatics cups fit), then for this k, no solution.
    # But we need at least 1 informatics cup. So if j < 1, this k is invalid.
    
    # Now iterate k from 1 to n
    for k in range(1, n + 1):
        w_phys = pref_phys[k]
        if w_phys > d:
            break # No more physics cups can fit
        
        # Decrease j as needed because width of physics increased
        while j >= 1 and (w_phys + pref_inf[j] > d):
            j -= 1
        
        if j < 1:
            # Cannot take any informatics cup with this k
            # Since k will only increase width, no need to check further k?
            # Actually, if we take more physics cups, width increases, so j will definitely be < 1.
            # So we can break.
            break
        
        # Calculate total significance
        total_sig = sum_phys[k] + sum_inf[j]
        if total_sig > max_significance:
            max_significance = total_sig
            
    print(max_significance)

if __name__ == '__main__':
    solve()