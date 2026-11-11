import sys
import heapq

def main():
    import sys
    import heapq
    
    def readints():
        return list(map(int, sys.stdin.read().split()))
    
    data = readints()
    n = data[0]
    a = data[1:]
    
    # Create a min-heap from the list a
    heapq.heapify(a)
    
    # Prepare the result list
    result = []
    
    # Distribute the ratings
    for i in range(1, n + 1):
        # Get the smallest element from the heap
        smallest = heapq.heappop(a)
        # Ensure the rating is at least i
        if smallest < i:
            smallest = i
        # Add the rating to the result
        result.append(smallest)
        # Push the new rating back into the heap
        heapq.heappush(a, smallest + 1)
    
    # Print the result
    print(" ".join(map(str, result)))

if __name__ == "__main__":
    main()