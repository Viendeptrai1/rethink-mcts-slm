import sys
from heapq import heappush, heappop

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    heights = list(map(int, data[1:n+1]))
    
    # Calculate the number of hills that are local maxima
    maxima = [True] * n
    for i in range(1, n-1):
        if heights[i] <= heights[i-1] or heights[i] <= heights[i+1]:
            maxima[i] = False
    if n > 1:
        maxima[0] = (heights[0] > heights[1])
        maxima[n-1] = (heights[n-1] > heights[n-2])
    
    # Count the initial number of maxima
    current_maxima = sum(maxima)
    
    # If the initial number of maxima is already enough, no work is needed
    if current_maxima >= (n + 1) // 2:
        result = [0] * ((n + 1) // 2)
        print(" ".join(map(str, result)))
        return
    
    # Create a min-heap of the heights of non-maxima hills
    heap = []
    for i in range(n):
        if not maxima[i]:
            heappush(heap, (heights[i], i))
    
    # Calculate the minimum time required for each k
    result = []
    for k in range(1, (n + 1) // 2 + 1):
        if current_maxima >= k:
            result.append(0)
            continue
        
        # We need to increase the number of maxima by (k - current_maxima)
        additional_maxima_needed = k - current_maxima
        time = 0
        
        while additional_maxima_needed > 0 and heap:
            height, index = heappop(heap)
            # Increase the height of this hill to make it a local maximum
            new_height = heights[index] + 1
            time += new_height - height
            
            # Update the maxima status of the neighbors
            if index > 0 and new_height > heights[index - 1]:
                maxima[index - 1] = True
                current_maxima += 1
                additional_maxima_needed -= 1
            if index < n - 1 and new_height > heights[index + 1]:
                maxima[index + 1] = True
                current_maxima += 1
                additional_maxima_needed -= 1
        
        # If we couldn't make enough maxima, it's impossible to build k houses
        if additional_maxima_needed > 0:
            result.append(-1)
        else:
            result.append(time)
    
    print(" ".join(map(str, result)))

if __name__ == "__main__":
    main()