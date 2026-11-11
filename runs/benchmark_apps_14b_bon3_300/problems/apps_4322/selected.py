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
    max_height = max(height_count.values())
    
    # Collect all heights that have the maximum frequency
    max_heights = [height for height, count in height_count.items() if count == max_height]
    
    # Sort the heights to form a balanced circle
    max_heights.sort()
    
    # Create the balanced circle
    result = []
    for height in max_heights:
        result.extend([height] * height_count[height])
    
    # Print the result
    print(len(result))
    print(' '.join(map(str, result)))

if __name__ == "__main__":
    main()