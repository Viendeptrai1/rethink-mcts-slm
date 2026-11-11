import sys
from collections import defaultdict

def max_balanced_circle(n, heights):
    # Count the frequency of each height
    freq = defaultdict(int)
    for height in heights:
        freq[height] += 1
    
    # Sort the unique heights
    unique_heights = sorted(freq.keys())
    
    max_length = 0
    best_circle = []
    
    # Try to form a balanced circle with consecutive heights
    for i in range(len(unique_heights)):
        current_length = 0
        current_circle = []
        
        # Start with the current height
        current_height = unique_heights[i]
        while current_height in freq and freq[current_height] > 0:
            current_circle.extend([current_height] * freq[current_height])
            current_length += freq[current_height]
            
            # Move to the next height if it exists and has a difference of at most 1
            if i + 1 < len(unique_heights) and unique_heights[i + 1] == current_height + 1:
                current_height += 1
            else:
                break
        
        # Check if the circle can be closed
        if current_length > 1 and abs(current_circle[0] - current_circle[-1]) <= 1:
            if current_length > max_length:
                max_length = current_length
                best_circle = current_circle
    
    return max_length, best_circle

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    heights = list(map(int, data[1:]))
    
    k, result = max_balanced_circle(n, heights)
    
    print(k)
    print(' '.join(map(str, result)))

if __name__ == "__main__":
    main()