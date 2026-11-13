import sys
import heapq

def alices_restaurant(n, m, a, c, orders):
    # Initialize the remaining dishes and the priority queue for the cheapest dishes
    remaining = a[:]
    pq = [(c[i], i) for i in range(n) if remaining[i] > 0]
    heapq.heapify(pq)
    
    results = []
    
    for t, d in orders:
        t -= 1  # Convert to 0-based index
        cost = 0
        
        # Serve the requested dishes of type t if available
        while d > 0 and remaining[t] > 0:
            cost += c[t]
            remaining[t] -= 1
            d -= 1
        
        # If there are still dishes requested but none of type t is left, serve from other types
        while d > 0 and pq:
            cheapest_cost, cheapest_type = heapq.heappop(pq)
            if remaining[cheapest_type] > 0:
                cost += cheapest_cost
                remaining[cheapest_type] -= 1
                d -= 1
                if remaining[cheapest_type] > 0:
                    heapq.heappush(pq, (c[cheapest_type], cheapest_type))
        
        # If there are still dishes requested but none are left, the customer leaves angrily
        if d > 0:
            cost = 0
        
        results.append(cost)
    
    return results

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    a = list(map(int, data[2:n+2]))
    c = list(map(int, data[n+2:2*n+2]))
    
    orders = []
    index = 2*n+2
    for _ in range(m):
        t = int(data[index])
        d = int(data[index+1])
        orders.append((t, d))
        index += 2
    
    results = alices_restaurant(n, m, a, c, orders)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()