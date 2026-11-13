import sys
import heapq

def alices_restaurant(n, m, a, c, orders):
    # Initialize the remaining dishes and the min-heap for the cheapest food
    remaining = a[:]
    min_heap = [(c[i], i) for i in range(n) if remaining[i] > 0]
    heapq.heapify(min_heap)
    
    results = []
    
    for t, d in orders:
        t -= 1  # Convert to 0-based index
        cost = 0
        
        # Serve the customer up to d dishes of the t-th kind
        for _ in range(d):
            if remaining[t] > 0:
                cost += c[t]
                remaining[t] -= 1
            elif min_heap:
                # Serve from the cheapest available food
                cheapest_cost, cheapest_index = heapq.heappop(min_heap)
                cost += cheapest_cost
                remaining[cheapest_index] -= 1
                if remaining[cheapest_index] > 0:
                    heapq.heappush(min_heap, (c[cheapest_index], cheapest_index))
            else:
                # No more dishes available
                cost = 0
                break
        
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