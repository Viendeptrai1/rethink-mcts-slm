import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
        m = int(next(iterator))
    except StopIteration:
        return

    # Store playlist segments: (end_time, song_index)
    # end_time is the cumulative duration up to the end of the current song's repetitions
    segments = []
    current_time = 0
    
    for i in range(1, n + 1):
        c = int(next(iterator))
        t = int(next(iterator))
        duration = c * t
        current_time += duration
        segments.append((current_time, i))
    
    # Read queries
    queries = []
    for _ in range(m):
        queries.append(int(next(iterator)))
    
    # Process queries
    results = []
    seg_idx = 0
    
    for v in queries:
        # Advance segment index until we find the segment that covers time v
        # Since queries are sorted, we can start from the last found position
        while seg_idx < n and segments[seg_idx][0] < v:
            seg_idx += 1
        
        # segments[seg_idx][0] >= v, so this is the correct song
        results.append(segments[seg_idx][1])
    
    # Print results
    print('\n'.join(map(str, results)))

if __name__ == '__main__':
    solve()