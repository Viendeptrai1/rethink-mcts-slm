import sys
from math import ceil

def main():
    import sys
    import heapq
    
    def readints():
        return list(map(int, sys.stdin.read().split()))
    
    data = readints()
    n = data[0]
    heights = data[1:]
    
    # Find peaks
    peaks = []
    for i in range(1, n-1):
        if heights[i] > heights[i-1] and heights[i] > heights[i+1]:
            peaks.append(i)
    
    # Add virtual peaks at the ends if necessary
    if heights[0] > heights[1]:
        peaks.insert(0, 0)
    if heights[-1] > heights[-2]:
        peaks.append(n-1)
    
    # Calculate the number of peaks we can have after each reduction
    num_peaks = len(peaks)
    reductions = [0] * ceil(n / 2)
    
    # Use a max heap to keep track of the largest reductions needed
    max_heap = []
    for peak in peaks:
        left_height = heights[peak-1] if peak > 0 else 0
        right_height = heights[peak+1] if peak < n-1 else 0
        reduction = min(heights[peak] - left_height - 1, heights[peak] - right_height - 1)
        if reduction > 0:
            heapq.heappush(max_heap, -reduction)
    
    # Calculate the minimum time for each k
    total_reduction = 0
    for k in range(1, ceil(n / 2) + 1):
        if len(max_heap) > 0:
            total_reduction -= heapq.heappop(max_heap)
        reductions[k-1] = total_reduction
    
    # Print the results
    print(' '.join(map(str, reductions)))

if __name__ == "__main__":
    main()