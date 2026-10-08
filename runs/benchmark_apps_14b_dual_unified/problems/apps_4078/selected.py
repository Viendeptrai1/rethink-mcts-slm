import sys
import heapq

def main():
    import sys
    import heapq
    
    def read_ints():
        return list(map(int, sys.stdin.readline().split()))
    
    n, m = read_ints()
    a = read_ints()
    segments = [read_ints() for _ in range(m)]
    
    # Create a list of events
    events = []
    for j, (l, r) in enumerate(segments):
        events.append((l-1, 1, j))  # Start of segment
        events.append((r, -1, j))   # End of segment
    
    # Sort events by position, start before end
    events.sort()
    
    # Initialize variables
    max_diff = 0
    best_segments = []
    current_segments = set()
    active_segments = []
    
    # Track the minimum and maximum values
    min_val = float('inf')
    max_val = float('-inf')
    
    for pos, typ, j in events:
        if typ == 1:
            # Start of a segment
            heapq.heappush(active_segments, (-a[pos], pos))
            current_segments.add(j)
        else:
            # End of a segment
            if -a[pos] == active_segments[0][0]:
                heapq.heappop(active_segments)
            current_segments.remove(j)
        
        # Update min and max values
        if active_segments:
            min_val = min(min_val, -active_segments[0][0])
            max_val = max(max_val, -active_segments[0][0])
        
        # Calculate the current difference
        current_diff = max_val - min_val
        
        # Check if this is the best solution so far
        if current_diff > max_diff:
            max_diff = current_diff
            best_segments = list(current_segments)
    
    # Output the result
    print(max_diff)
    print(len(best_segments))
    print(*[x+1 for x in sorted(best_segments)])

if __name__ == "__main__":
    main()