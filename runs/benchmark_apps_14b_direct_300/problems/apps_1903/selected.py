import sys
import heapq

def max_significance(n, m, d, physics_cups, informatics_cups):
    # Sort cups by significance in descending order
    physics_cups.sort(key=lambda x: -x[0])
    informatics_cups.sort(key=lambda x: -x[0])
    
    # Initialize variables
    max_significance = 0
    physics_heap = []
    informatics_heap = []
    
    # Add all Physics cups to the heap
    for c, w in physics_cups:
        heapq.heappush(physics_heap, (-c, w))
    
    # Add all Informatics cups to the heap
    for c, w in informatics_cups:
        heapq.heappush(informatics_heap, (-c, w))
    
    # Initialize current width and significance
    current_width = 0
    current_significance = 0
    
    # Try to add the most significant Physics cup
    if physics_heap:
        c, w = heapq.heappop(physics_heap)
        current_width += w
        current_significance -= c
    
    # Try to add the most significant Informatics cup
    if informatics_heap:
        c, w = heapq.heappop(informatics_heap)
        current_width += w
        current_significance -= c
    
    # If we can't add both types of cups, return 0
    if current_width > d:
        return 0
    
    # Try to add more cups while respecting the width constraint
    while physics_heap or informatics_heap:
        if not physics_heap:
            next_c, next_w = heapq.heappop(informatics_heap)
        elif not informatics_heap:
            next_c, next_w = heapq.heappop(physics_heap)
        else:
            if physics_heap[0][0] < informatics_heap[0][0]:
                next_c, next_w = heapq.heappop(physics_heap)
            else:
                next_c, next_w = heapq.heappop(informatics_heap)
        
        if current_width + next_w <= d:
            current_width += next_w
            current_significance -= next_c
        else:
            break
    
    return current_significance

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    m = int(data[index + 1])
    d = int(data[index + 2])
    index += 3
    
    physics_cups = []
    for _ in range(n):
        c = int(data[index])
        w = int(data[index + 1])
        physics_cups.append((c, w))
        index += 2
    
    informatics_cups = []
    for _ in range(m):
        c = int(data[index])
        w = int(data[index + 1])
        informatics_cups.append((c, w))
        index += 2
    
    result = max_significance(n, m, d, physics_cups, informatics_cups)
    print(result)

if __name__ == "__main__":
    main()