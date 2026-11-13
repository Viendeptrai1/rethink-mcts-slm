import sys

def main():
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    
    n = int(next(iterator))
    m = int(next(iterator))
    
    # Store cumulative end times for each song
    # We only need the end time to binary search
    end_times = []
    current_time = 0
    
    # Read n lines of (c_i, t_i)
    for i in range(1, n + 1):
        c = int(next(iterator))
        t = int(next(iterator))
        duration = c * t
        current_time += duration
        end_times.append(current_time)
    
    # Read m query moments
    results = []
    for _ in range(m):
        v = int(next(iterator))
        
        # Binary search to find the song
        # We need the largest index i such that end_times[i] >= v
        # Since end_times is sorted, we can use bisect_right logic manually
        
        left = 0
        right = n - 1
        ans = n - 1 # Default to last song if not found (though guaranteed to exist)
        
        while left <= right:
            mid = (left + right) // 2
            if end_times[mid] >= v:
                ans = mid
                right = mid - 1
            else:
                left = mid + 1
        
        # Convert 0-based index to 1-based song number
        results.append(str(ans + 1))
    
    sys.stdout.write('\n'.join(results) + '\n')

if __name__ == "__main__":
    main()