import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    n = int(next(iterator))
    m = int(next(iterator))
    
    # We need to store the end time of each song's block
    # end_times[i] will store the cumulative time up to and including song i+1
    end_times = []
    current_time = 0
    
    for i in range(n):
        c = int(next(iterator))
        t = int(next(iterator))
        duration = c * t
        current_time += duration
        end_times.append(current_time)
    
    # Process queries
    results = []
    for _ in range(m):
        v = int(next(iterator))
        
        # Binary search to find the song index
        # We need the largest index i such that end_times[i] >= v
        # Since end_times is sorted, we can use bisect_right and adjust
        
        # Using manual binary search for clarity and no extra imports
        left = 0
        right = n - 1
        ans = 0
        
        while left <= right:
            mid = (left + right) // 2
            if end_times[mid] >= v:
                ans = mid
                right = mid - 1
            else:
                left = mid + 1
        
        # Convert 0-based index to 1-based song number
        results.append(str(ans + 1))
    
    print('\n'.join(results))

if __name__ == '__main__':
    solve()