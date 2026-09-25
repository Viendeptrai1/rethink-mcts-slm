import sys

def main():
    import sys
    import heapq
    
    def read_ints():
        return list(map(int, sys.stdin.read().split()))
    
    data = read_ints()
    n = data[0]
    a = data[1:]
    
    # Find the minimum and maximum values in the array
    min_a = min(a)
    max_a = max(a)
    
    # If all elements are the same, the instability is 0
    if min_a == max_a:
        print(0)
        return
    
    # Create two heaps: one for the smallest elements and one for the largest elements
    min_heap = []
    max_heap = []
    
    for num in a:
        heapq.heappush(min_heap, num)
        heapq.heappush(max_heap, -num)
    
    # Remove the smallest element and calculate the instability
    min_removed = heapq.heappop(min_heap)
    instability_min_removed = max_a - min_heap[0]
    
    # Remove the largest element and calculate the instability
    max_removed = -heapq.heappop(max_heap)
    instability_max_removed = -max_heap[0] - min_a
    
    # The minimum possible instability is the smaller of the two
    print(min(instability_min_removed, instability_max_removed))

if __name__ == "__main__":
    main()