import heapq
import sys

def main():
    import sys
    import heapq
    
    def read_ints():
        return list(map(int, sys.stdin.readline().split()))
    
    n, m = read_ints()
    a = read_ints()
    c = read_ints()
    
    # Initialize the heap with (cost, index) pairs
    heap = [(c[i], i) for i in range(n)]
    heapq.heapify(heap)
    
    # Initialize the remaining dishes
    remaining = a[:]
    
    results = []
    
    for _ in range(m):
        t_j, d_j = read_ints()
        t_j -= 1  # Convert to 0-based index
        
        total_cost = 0
        
        while d_j > 0:
            if remaining[t_j] > 0:
                # Serve the requested dish
                remaining[t_j] -= 1
                total_cost += c[t_j]
                d_j -= 1
            else:
                # Find the cheapest available dish
                while heap and remaining[heap[0][1]] == 0:
                    heapq.heappop(heap)
                if heap:
                    cheapest_cost, cheapest_index = heapq.heappop(heap)
                    remaining[cheapest_index] -= 1
                    total_cost += cheapest_cost
                    d_j -= 1
                    # Push back the cheapest dish if it still has remaining
                    if remaining[cheapest_index] > 0:
                        heapq.heappush(heap, (cheapest_cost, cheapest_index))
                else:
                    # No more dishes available
                    break
        
        results.append(total_cost)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()