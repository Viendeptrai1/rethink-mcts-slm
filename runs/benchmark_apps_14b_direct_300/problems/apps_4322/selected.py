import sys
from collections import defaultdict

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    heights = list(map(int, data[1:]))
    
    # Count occurrences of each height
    height_count = defaultdict(int)
    for height in heights:
        height_count[height] += 1
    
    # Find the most frequent height
    max_height = max(height_count, key=height_count.get)
    max_count = height_count[max_height]
    
    # Check if we can form a balanced circle with the most frequent height
    if max_count >= 2:
        # We can form a circle with all occurrences of the most frequent height
        result = [max_height] * max_count
    else:
        # We need to find the longest sequence of consecutive heights
        # Create a list of unique heights sorted
        unique_heights = sorted(set(heights))
        
        # Find the longest sequence of consecutive heights
        max_length = 1
        current_length = 1
        best_start = 0
        
        for i in range(1, len(unique_heights)):
            if unique_heights[i] == unique_heights[i - 1] + 1:
                current_length += 1
            else:
                if current_length > max_length:
                    max_length = current_length
                    best_start = i - current_length
                current_length = 1
        
        # Check the last sequence
        if current_length > max_length:
            max_length = current_length
            best_start = len(unique_heights) - current_length
        
        # Construct the result
        result = []
        for i in range(best_start, best_start + max_length):
            height = unique_heights[i]
            result.extend([height] * height_count[height])
    
    # Print the result
    print(len(result))
    print(" ".join(map(str, result)))

if __name__ == "__main__":
    main()