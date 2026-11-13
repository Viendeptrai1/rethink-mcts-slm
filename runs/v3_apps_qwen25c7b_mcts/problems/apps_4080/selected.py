import heapq

def max_difference(n, m, a, segments):
    # Calculate the initial difference
    current_max = max(a)
    current_min = min(a)
    current_diff = current_max - current_min
    
    # Priority queue to store segments based on their impact
    pq = []
    
    for i, (l, r) in enumerate(segments):
        # Calculate the impact of the segment
        impact = (current_max - current_min) + (r - l + 1)
        heapq.heappush(pq, (-impact, i))
    
    selected_segments = []
    new_diff = current_diff
    
    while pq:
        _, idx = heapq.heappop(pq)
        l, r = segments[idx]
        
        # Apply the segment
        for j in range(l - 1, r):
            a[j] -= 1
        
        # Update the new maximum and minimum values
        new_max = max(a)
        new_min = min(a)
        new_diff = new_max - new_min
        
        # Check if the difference increased
        if new_diff > current_diff:
            selected_segments.append(idx + 1)
            current_diff = new_diff
        else:
            # Revert the changes if the difference did not increase
            for j in range(l - 1, r):
                a[j] += 1
    
    return current_diff, len(selected_segments), selected_segments

# Input reading
n, m = map(int, input().split())
a = list(map(int, input().split()))
segments = [tuple(map(int, input().split())) for _ in range(m)]

# Output the result
result_diff, result_count, result_segments = max_difference(n, m, a, segments)
print(result_diff)
print(result_count)
print(*result_segments)