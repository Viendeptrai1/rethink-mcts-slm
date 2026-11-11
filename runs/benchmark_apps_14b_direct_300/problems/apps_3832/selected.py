import sys
from math import ceil

def main():
    import sys
    import heapq
    
    def read_ints():
        return list(map(int, sys.stdin.readline().split()))
    
    n = read_ints()[0]
    heights = read_ints()
    
    # Find all peaks
    peaks = []
    for i in range(1, n-1):
        if heights[i] > heights[i-1] and heights[i] > heights[i+1]:
            peaks.append((heights[i], i))
    
    # Add virtual peaks at the ends
    if n > 1 and heights[0] > heights[1]:
        peaks.append((heights[0], 0))
    if n > 1 and heights[-1] > heights[-2]:
        peaks.append((heights[-1], n-1))
    
    # Sort peaks by height in descending order
    peaks.sort(reverse=True)
    
    # Calculate the minimum time required for each k
    result = [0] * ceil(n / 2)
    heap = []
    
    for k in range(1, len(result) + 1):
        while len(heap) < k:
            if not peaks:
                break
            heapq.heappush(heap, peaks.pop()[0])
        
        if len(heap) < k:
            result[k-1] = -1
        else:
            result[k-1] = sum(heap) - k * min(heap)
    
    print(" ".join(map(str, result)))

if __name__ == "__main__":
    main()