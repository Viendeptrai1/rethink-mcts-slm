import sys
import heapq

def main():
    import sys
    import heapq
    
    def readints():
        return list(map(int, sys.stdin.read().split()))
    
    data = readints()
    N = data[0]
    A = data[1:]
    
    # Use a min-heap to keep track of the smallest elements
    heapq.heapify(A)
    
    while len(A) > 1:
        # Extract the two smallest elements
        x = heapq.heappop(A)
        y = heapq.heappop(A)
        
        # The smaller monster attacks the larger one
        if x < y:
            heapq.heappush(A, y - x)
        else:
            heapq.heappush(A, x - y)
    
    # The last remaining element is the minimum possible final health
    print(A[0])

if __name__ == "__main__":
    main()