import sys

# Increase recursion depth just in case, though we will use iterative approach
sys.setrecursionlimit(200000)

def solve():
    # Read all input from stdin at once
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
        m = int(next(iterator))
        
        a = []
        for _ in range(n):
            a.append(int(next(iterator)))
            
        c = []
        for _ in range(n):
            c.append(int(next(iterator)))
            
        orders = []
        for _ in range(m):
            t = int(next(iterator))
            d = int(next(iterator))
            orders.append((t, d))
            
    except StopIteration:
        return

    # We need to efficiently find the cheapest available dish.
    # Since the set of available dishes changes (depleting to 0), we can use a min-heap.
    # However, simply removing from heap one by one might be slow if many items are 0.
    # Strategy:
    # 1. Create a list of (cost, index) for all food items.
    # 2. Sort this list by cost, then by index.
    # 3. Use a pointer (heap_index) to track the current cheapest candidate.
    # 4. Maintain a variable `total_remaining` = sum(a).
    # 5. When a customer orders specific food:
    #    - If the requested food has remaining stock, serve as much as possible.
    #    - If not, fall back to the cheapest available food (starting from heap_index).
    #    - While serving from cheapest, if a food stock drops to 0, increment heap_index to skip it.
    #    - Stop if total_remaining becomes 0 (customer leaves, cost 0).

    # Sort food items by (cost, index)
    # We store tuples (cost, original_index)
    food_items = []
    for i in range(n):
        food_items.append((c[i], i))
    
    food_items.sort()
    
    # Pointers and state
    heap_ptr = 0
    current_total_remaining = sum(a)
    
    results = []
    
    # Pre-calculate initial sums? No need, we track dynamically.
    
    for t_idx, d in orders:
        # t_idx is 1-based in input, convert to 0-based
        t_idx -= 1
        
        if current_total_remaining == 0:
            results.append(0)
            continue
            
        cost_customer = 0
        served_count = 0
        possible = True
        
        # Step 1: Try to fulfill the order with the specific food type
        if a[t_idx] > 0:
            take = min(d, a[t_idx])
            cost_customer += take * c[t_idx]
            a[t_idx] -= take
            d -= take
            served_count += take
            current_total_remaining -= take
            
            if d == 0:
                # Order fulfilled
                results.append(cost_customer)
                continue
        
        # Step 2: If still need more, fallback to cheapest available
        if d > 0:
            while d > 0 and heap_ptr < n:
                # Get the cheapest available food
                cost_min, idx_min = food_items[heap_ptr]
                
                if a[idx_min] == 0:
                    # This food is exhausted, move pointer
                    heap_ptr += 1
                    continue
                
                # Serve as much as possible from this cheapest food
                take = min(d, a[idx_min])
                cost_customer += take * cost_min
                a[idx_min] -= take
                d -= take
                served_count += take
                current_total_remaining -= take
                
                if a[idx_min] == 0:
                    # Stock exhausted, move pointer for next time
                    heap_ptr += 1
                
                if d == 0:
                    break
            
            if d > 0:
                # Cannot fulfill the rest
                possible = False
        
        if possible:
            results.append(cost_customer)
        else:
            results.append(0)

    for res in results:
        print(res)

if __name__ == "__main__":
    solve()