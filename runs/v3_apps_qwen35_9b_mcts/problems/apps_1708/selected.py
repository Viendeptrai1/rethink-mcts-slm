import sys
import heapq

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
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

    # Adjust to 0-based indexing
    # a[i] is remaining count for food i
    # c[i] is cost for food i
    
    # We need a min-heap of (cost, index) for available foods
    # We also need to track which foods are currently available (count > 0)
    
    # Initial heap construction
    heap = []
    for i in range(n):
        if a[i] > 0:
            heapq.heappush(heap, (c[i], i))
            
    # To efficiently handle the case where the requested food is cheaper than the heap top,
    # we can't just rely on the heap for the primary request. We must check the requested food first.
    # However, for the fallback (cheapest available), the heap is perfect.
    # The tricky part is: if the requested food is exhausted, we need to find the new cheapest.
    # The heap might contain indices that are now exhausted (count == 0).
    # So we need a lazy deletion strategy for the heap.
    
    # Let's maintain:
    # 1. `a`: current remaining counts.
    # 2. `heap`: min-heap of (cost, index) for foods with a[i] > 0.
    # 3. When popping from heap, if a[index] == 0, discard and pop again.
    
    # But there's a catch: if the requested food `t` is NOT the cheapest, but we serve from it,
    # and it gets exhausted, we then need to serve the rest from the cheapest available.
    # The cheapest available is at the top of the heap (after cleaning).
    # What if the requested food `t` IS the cheapest? Then we serve from `t` until exhausted,
    # and then continue serving from the next cheapest (which might be `t` if we didn't exhaust it,
    # or another food).
    
    # Algorithm for each customer (t, d):
    # 1. Check if total remaining food in the system is 0. If so, cost = 0.
    # 2. Serve as many as possible from `t` (up to d and up to a[t]).
    #    - If a[t] > 0:
    #      - take = min(d, a[t])
    #      - cost += take * c[t]
    #      - a[t] -= take
    #      - d -= take
    #      - If a[t] becomes 0, we might need to remove `t` from the heap if it's there.
    #        Actually, we don't need to remove immediately; lazy deletion handles it.
    #        But if `t` was in the heap and now a[t] == 0, future heap pops will skip it.
    # 3. If d > 0 (still need more food):
    #    - We need to serve the remaining `d` from the cheapest available food globally.
    #    - The cheapest available is at the top of the heap (after cleaning stale entries).
    #    - We might need to serve from multiple food types if one type runs out.
    #    - Loop:
    #      - Clean heap top: while heap and a[heap[0][1]] == 0: pop.
    #      - If heap is empty: break (customer leaves angrily, cost remains what it is).
    #      - Get (cost_val, idx) = heap[0]
    #      - take = min(d, a[idx])
    #      - cost += take * cost_val
    #      - a[idx] -= take
    #      - d -= take
    #      - If d == 0: break
    #      - If a[idx] == 0:
    #          - We exhausted this food. We need to pop it from the heap to make room for the next cheapest.
    #          - heapq.heappop(heap)
    #          - Continue loop.
    #      - Else:
    #          - We still have stock in this food, but we satisfied the customer's demand.
    #          - We don't need to pop it yet (it stays in heap for future customers).
    #          - Break.
    
    # Wait, there is a subtle issue in step 3.
    # If the requested food `t` was NOT the cheapest, we served from `t` first.
    # Then we look for the cheapest. The cheapest might be `t` itself if we didn't exhaust it?
    # No, if we didn't exhaust `t` in step 2, then `t` still has stock.
    # But if `t` was not the cheapest, then the cheapest is some other food `k`.
    # So we serve from `k`.
    # What if `t` WAS the cheapest? Then in step 2 we served from `t`.
    # If `t` is still not exhausted, then `t` is still the cheapest.
    # Should we serve the rest from `t`? Yes.
    # But my logic in step 3 says "serve from cheapest available".
    # If `t` is still available and is the cheapest, the heap top will be `t`.
    # So the loop in step 3 will naturally pick `t` again.
    # This is correct.
    
    # However, there is one more edge case:
    # What if the requested food `t` is cheaper than the current heap top?
    # Example: t=1, cost=10, a[1]=5. Heap top is (cost=20, idx=2).
    # Customer orders 3 of type 1.
    # Step 2: Serve 3 from type 1. a[1] becomes 2. d becomes 0. Done.
    # Correct.
    
    # Example: t=1, cost=20, a[1]=5. Heap top is (cost=10, idx=2).
    # Customer orders 3 of type 1.
    # Step 2: Serve 3 from type 1. a[1] becomes 2. d becomes 0. Done.
    # Correct.
    
    # Example: t=1, cost=20, a[1]=2. Heap top is (cost=10, idx=2).
    # Customer orders 5 of type 1.
    # Step 2: Serve 2 from type 1. a[1] becomes 0. d becomes 3.
    # Step 3: Clean heap. Top is (10, 2). a[2] > 0.
    # Serve min(3, a[2]) from type 2.
    # Correct.
    
    # One optimization: If the requested food `t` is NOT in the heap (because a[t] == 0),
    # we skip step 2 entirely (or take 0).
    # If `t` is in the heap, we serve from it.
    # But wait, if `t` is in the heap, it means a[t] > 0.
    # So step 2 is valid.
    
    # Is it possible that after serving from `t` in step 2, `t` becomes the cheapest?
    # Yes, if `t` was not the cheapest before, but after serving from it, it's still the cheapest?
    # No, serving from `t` reduces its count, it doesn't change its cost.
    # So if `t` was not the cheapest, it remains not the cheapest (unless it was the only one left? No).
    # The cost is constant. The relative order of costs doesn't change.
    # So if `t` was not the cheapest, it won't become the cheapest by reducing its count.
    # The only way `t` becomes the cheapest is if it was already the cheapest.
    # So if `t` is not the cheapest, we serve from `t` (if available), then switch to the global cheapest.
    # If `t` is the cheapest, we serve from `t` until exhausted, then switch to the next cheapest.
    # My logic handles both cases correctly because the heap top will reflect the global minimum.
    
    # Wait, there is a potential performance issue.
    # If we have many customers and we keep popping from the heap in step 3, it's O(log N) per pop.
    # Total operations: sum of d_j can be large, but we only pop when a food is exhausted.
    # Each food is exhausted at most once. So total pops from heap is at most N.
    # The inner loop runs at most N times across all customers (since each iteration either satisfies the customer or exhausts a food).
    # Actually, the loop runs:
    # - Once to pick a food and satisfy the customer (break).
    # - Or multiple times to exhaust several foods.
    # Since each food is exhausted once globally, the total number of "exhaust" iterations across all customers is N.
    # The "satisfy" iterations is M.
    # So total complexity is O(M log N + N log N). This is efficient enough.
    
    # One detail: "If there are multiple cheapest kinds of food, the one with the smallest index among the cheapest will be served."
    # Our heap stores (cost, index). Python's heapq compares tuples element by element.
    # So (cost, index) will naturally sort by cost, then by index.
    # This matches the requirement perfectly.
    
    # Another detail: "If there are no more dishes at all, the customer will leave angrily. Therefore, no matter how many dishes are served previously, the cost for the customer is 0."
    # This means if at any point we cannot serve a dish (heap empty and d > 0), the total cost for that customer becomes 0.
    # My logic: if heap is empty and d > 0, we break. Then we print cost.
    # But the problem says cost becomes 0.
    # So if we break due to empty heap, we must reset cost to 0.
    
    results = []
    
    for t, d in orders:
        t_idx = t - 1
        total_cost = 0
        possible = True
        
        # Check if total remaining food is 0
        # We can maintain a global sum of 'a', but recalculating or maintaining it is fine.
        # Let's just check if heap is empty and a[t_idx] == 0?
        # No, there might be other foods.
        # We can maintain a variable `total_remaining` initialized to sum(a).
        # Decrement it when we serve.
        # If total_remaining == 0, then customer leaves angrily.
        
        # Let's refactor to maintain total_remaining.
        pass

    # Re-implementing with total_remaining tracking
    total_remaining = sum(a)
    
    # Re-initialize heap
    heap = []
    for i in range(n):
        if a[i] > 0:
            heapq.heappush(heap, (c[i], i))
            
    for t, d in orders:
        t_idx = t - 1
        customer_cost = 0
        
        # If no food left at all
        if total_remaining == 0:
            results.append(0)
            continue
            
        # Step 1: Serve from requested food t
        if a[t_idx] > 0:
            take = min(d, a[t_idx])
            customer_cost += take * c[t_idx]
            a[t_idx] -= take
            d -= take
            total_remaining -= take
            
            # If a[t_idx] becomes 0, we don't need to remove from heap immediately (lazy deletion)
            # But if it was in the heap, it will be skipped later.
            # However, if we need to serve more (d > 0), we will look at the heap.
            # If t_idx is the cheapest, and we exhausted it, the heap top might be stale.
            # The cleaning loop in Step 2 will handle it.
        
        # Step 2: Serve remaining d from cheapest available
        if d > 0:
            while d > 0:
                # Clean heap
                while heap and a[heap[0][1]] == 0:
                    heapq.heappop(heap)
                
                if not heap:
                    # No food left
                    customer_cost = 0
                    possible = False
                    break
                
                cost_val, idx = heap[0]
                take = min(d, a[idx])
                customer_cost += take * cost_val
                a[idx] -= take
                d -= take
                total_remaining -= take
                
                if d == 0:
                    break
                
                # If we exhausted this food, pop it from heap
                if a[idx] == 0:
                    heapq.heappop(heap)
                # Else: we satisfied the customer, break loop.
                # Note: we do NOT pop here because this food still has stock and might be the cheapest for next customer.
        
        if not possible:
            results.append(0)
        else:
            results.append(customer_cost)

    for res in results:
        print(res)

if __name__ == '__main__':
    solve()