import sys
import heapq

def main():
    import sys
    import heapq
    
    def read_ints():
        return list(map(int, sys.stdin.read().split()))
    
    data = read_ints()
    N = data[0]
    A = data[1:]
    
    # Use a min-heap to keep track of the smallest health values
    heapq.heapify(A)
    
    while len(A) > 1:
        # Pop the two smallest elements
        smallest = heapq.heappop(A)
        second_smallest = heapq.heappop(A)
        
        # The smaller monster attacks the larger one
        new_health = second_smallest - smallest
        
        # If the new health is positive, push it back into the heap
        if new_health > 0:
            heapq.heappush(A, new_health)
    
    # The last remaining element in the heap is the minimum possible final health
    print(A[0])

if __name__ == "__main__":
    main()