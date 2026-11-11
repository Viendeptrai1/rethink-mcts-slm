import sys
import heapq

def max_significance(n, m, d, physics_cups, informatics_cups):
    # Sort cups by significance in descending order
    physics_cups.sort(key=lambda x: -x[0])
    informatics_cups.sort(key=lambda x: -x[0])
    
    # Initialize heaps for Physics and Informatics cups
    physics_heap = []
    informatics_heap = []
    
    # Add all cups to their respective heaps
    for c, w in physics_cups:
        heapq.heappush(physics_heap, (-c, w))
    for c, w in informatics_cups:
        heapq.heappush(informatics_heap, (-c, w))
    
    # Initialize variables to track the best solution
    max_significance = 0
    
    # Try to include at least one cup from each subject
    while physics_heap and informatics_heap:
        # Get the most significant cup from each subject
        p_c, p_w = heapq.heappop(physics_heap)
        i_c, i_w = heapq.heappop(informatics_heap)
        
        # Calculate the total width and significance
        total_width = p_w + i_w
        total_significance = -p_c - i_c
        
        # If the total width exceeds the shelf width, break
        if total_width > d:
            break
        
        # Update the maximum significance
        max_significance = max(max_significance, total_significance)
        
        # Try to add more cups from each subject while maintaining the constraints
        remaining_width = d - total_width
        current_significance = total_significance
        
        # Try adding more Physics cups
        while physics_heap and physics_heap[0][1] <= remaining_width:
            c, w = heapq.heappop(physics_heap)
            current_significance += -c
            remaining_width -= w
            max_significance = max(max_significance, current_significance)
        
        # Restore the Physics heap to its original state
        heapq.heappush(physics_heap, (p_c, p_w))
        
        # Try adding more Informatics cups
        while informatics_heap and informatics_heap[0][1] <= remaining_width:
            c, w = heapq.heappop(informatics_heap)
            current_significance += -c
            remaining_width -= w
            max_significance = max(max_significance, current_significance)
        
        # Restore the Informatics heap to its original state
        heapq.heappush(informatics_heap, (i_c, i_w))
    
    return max_significance

# Read input
n, m, d = map(int, input().split())
physics_cups = [tuple(map(int, input().split())) for _ in range(n)]
informatics_cups = [tuple(map(int, input().split())) for _ in range(m)]

# Print the result
print(max_significance(n, m, d, physics_cups, informatics_cups))