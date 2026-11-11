import sys
import heapq

def main():
    def read_ints():
        return list(map(int, sys.stdin.readline().split()))
    
    n, m = read_ints()
    a = read_ints()
    c = read_ints()
    
    # Initialize the heap with (cost, index) pairs
    heap = [(c[i], i) for i in range(n)]
    heapq.heapify(heap)
    
    # Initialize the remain array
    r = a[:]
    
    # Process each customer
    results = []
    for _ in range(m):
        t_j, d_j = read_ints()
        t_j -= 1  # Convert to 0-based index
        
        cost = 0
        while d_j > 0:
            if r[t_j] > 0:
                # Serve from the requested type
                cost += c[t_j]
                r[t_j] -= 1
                d_j -= 1
            else:
                # Find the cheapest available type
                while heap and r[heap[0][1]] == 0:
                    heapq.heappop(heap)
                if heap:
                    cheapest_cost, cheapest_index = heapq.heappop(heap)
                    cost += cheapest_cost
                    r[cheapest_index] -= 1
                    d_j -= 1
                    # Push back the cheapest type if it still has remaining dishes
                    if r[cheapest_index] > 0:
                        heapq.heappush(heap, (cheapest_cost, cheapest_index))
                else:
                    # No more dishes available
                    cost = 0  # Set cost to 0 if no more dishes can be served
                    break
        
        results.append(cost)
    
    # Print the results
    for result in results:
        print(result)

if __name__ == "__main__":
    main()