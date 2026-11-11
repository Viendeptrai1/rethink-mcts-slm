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
    
    # Try to find the maximum significance
    while physics_heap and informatics_heap:
        # Get the most significant Physics and Informatics cups
        physics_c, physics_w = heapq.heappop(physics_heap)
        informatics_c, informatics_w = heapq.heappop(informatics_heap)
        
        # Check if we can place both cups on the shelf
        if physics_w + informatics_w <= d:
            max_significance = -physics_c - informatics_c
            break
        
        # If we can't place both, try to place the most significant one
        if physics_w <= d:
            max_significance = -physics_c
            break
        
        if informatics_w <= d:
            max_significance = -informatics_c
            break
        
        # If neither can be placed, push them back and break
        heapq.heappush(physics_heap, (physics_c, physics_w))
        heapq.heappush(informatics_heap, (informatics_c, informatics_w))
        break
    
    return max_significance

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    d = int(data[2])
    
    physics_cups = []
    informatics_cups = []
    
    index = 3
    for _ in range(n):
        c = int(data[index])
        w = int(data[index + 1])
        physics_cups.append((c, w))
        index += 2
    
    for _ in range(m):
        c = int(data[index])
        w = int(data[index + 1])
        informatics_cups.append((c, w))
        index += 2
    
    result = max_significance(n, m, d, physics_cups, informatics_cups)
    print(result)

if __name__ == "__main__":
    main()