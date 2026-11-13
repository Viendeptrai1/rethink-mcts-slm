import heapq
from typing import List, Tuple

def alices_restaurant(n: int, m: int, a: List[int], c: List[int], orders: List[Tuple[int, int]]) -> List[int]:
    # Initialize remaining dishes and cost heap
    remaining = a.copy()
    cost_heap = [(c[i], i) for i in range(n)]
    heapq.heapify(cost_heap)

    # Initialize results
    results = []

    for t, d in orders:
        t -= 1  # Convert to 0-based index
        cost = 0

        # Serve dishes of the requested type if available
        for _ in range(d):
            if remaining[t] > 0:
                cost += c[t]
                remaining[t] -= 1
            else:
                # Find the cheapest available dish
                while cost_heap and remaining[cost_heap[0][1]] == 0:
                    heapq.heappop(cost_heap)
                
                if not cost_heap:
                    # No dishes left
                    cost = 0
                    break
                
                cheapest_cost, cheapest_index = heapq.heappop(cost_heap)
                cost += cheapest_cost
                remaining[cheapest_index] -= 1
                if remaining[cheapest_index] > 0:
                    heapq.heappush(cost_heap, (c[cheapest_index], cheapest_index))

        results.append(cost)

    return results

# Read input
n, m = map(int, input().split())
a = list(map(int, input().split()))
c = list(map(int, input().split()))
orders = [tuple(map(int, input().split())) for _ in range(m)]

# Solve and print output
result = alices_restaurant(n, m, a, c, orders)
for cost in result:
    print(cost)