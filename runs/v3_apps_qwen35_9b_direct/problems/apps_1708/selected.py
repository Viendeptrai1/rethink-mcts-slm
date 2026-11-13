import sys
import heapq

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    n = int(next(iterator))
    m = int(next(iterator))
    
    a = []
    for _ in range(n):
        a.append(int(next(iterator)))
        
    c = []
    for _ in range(n):
        c.append(int(next(iterator)))
        
    # Create a min-heap of (cost, index) for available dishes
    # We only add items to the heap if they have remaining stock > 0
    # However, since stock changes, we need a way to efficiently get the cheapest available.
    # Strategy: Maintain a heap of (cost, index) for all items. 
    # When an item is exhausted, we don't remove it from the heap immediately (lazy deletion).
    # Instead, when popping from the heap, check if the item still has stock.
    
    heap = []
    for i in range(n):
        heapq.heappush(heap, (c[i], i))
        
    # We also need to track current remaining amounts
    # a is already tracking remaining amounts
    
    results = []
    
    for _ in range(m):
        t = int(next(iterator)) - 1  # 0-indexed
        d = int(next(iterator))
        
        total_cost = 0
        served = 0
        
        # First, try to serve from the requested kind
        if a[t] > 0:
            take = min(d, a[t])
            total_cost += take * c[t]
            a[t] -= take
            served += take
            d -= take
        
        # If still need more, serve from cheapest available
        while d > 0:
            # Get cheapest available
            while heap:
                cost, idx = heapq.heappop(heap)
                if a[idx] > 0:
                    # This item is available
                    break
                else:
                    # This item is exhausted, continue searching
                    continue
            
            if not heap:
                # No more food available
                break
            
            cost, idx = heap[0] # Peek
            # Actually we popped above, so we need to push back if we don't use it?
            # No, the logic above: we pop until we find a valid one.
            # Let's restructure the loop to be cleaner.
            
            # Re-do the inner loop logic properly
            pass
        
        # Let's rewrite the inner loop logic cleanly
        # We need to serve 'd' more dishes
        
        # We will use a temporary list to collect the valid cheapest items we encounter
        # But since we need to serve potentially many dishes, we should just pop valid ones.
        
        # Reset the heap pointer logic? No, heap is persistent.
        # We need to handle the case where we pop an exhausted item.
        
        # Let's restart the serving logic for this customer
        d_needed = d
        current_cost = 0
        
        # 1. Serve from requested type
        if a[t] > 0:
            take = min(d_needed, a[t])
            current_cost += take * c[t]
            a[t] -= take
            d_needed -= take
        
        # 2. Serve from cheapest available
        while d_needed > 0:
            # Find the next valid cheapest item
            found = False
            while heap:
                cost, idx = heapq.heappop(heap)
                if a[idx] > 0:
                    # Valid item found
                    take = min(d_needed, a[idx])
                    current_cost += take * cost
                    a[idx] -= take
                    d_needed -= take
                    if d_needed == 0:
                        found = True
                        break
                    # If we used some but not all, we need to push this item back with remaining stock
                    # But wait, if we push back, it might not be the cheapest anymore? 
                    # No, the cost is fixed. If we have remaining stock, it's still the same cost.
                    # So we push it back.
                    heapq.heappush(heap, (cost, idx))
                    break
                # else: exhausted, discard
            
            if not found:
                # Heap empty or all exhausted
                break
        
        if d_needed > 0:
            # Customer leaves angrily
            results.append(0)
        else:
            results.append(current_cost)
            
    for res in results:
        print(res)

if __name__ == '__main__':
    solve()