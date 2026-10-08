import sys
from collections import Counter

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    heights = list(map(int, data[1:]))
    
    # Count the frequency of each height
    height_count = Counter(heights)
    
    # Find the most frequent height
    most_common_height, _ = height_count.most_common(1)[0]
    
    # Create a list of heights sorted by their values
    sorted_heights = sorted(heights)
    
    # Initialize variables to track the best circle
    max_length = 0
    best_circle = []
    
    # Try to form a circle with heights differing by at most 1
    for i in range(n):
        current_height = sorted_heights[i]
        current_circle = [current_height]
        
        # Extend the circle to the right
        j = i + 1
        while j < n and abs(sorted_heights[j] - current_circle[-1]) <= 1:
            current_circle.append(sorted_heights[j])
            j += 1
        
        # Extend the circle to the left
        k = i - 1
        while k >= 0 and abs(sorted_heights[k] - current_circle[0]) <= 1:
            current_circle.insert(0, sorted_heights[k])
            k -= 1
        
        # Check if the circle is valid (first and last elements differ by at most 1)
        if abs(current_circle[0] - current_circle[-1]) <= 1:
            if len(current_circle) > max_length:
                max_length = len(current_circle)
                best_circle = current_circle
    
    # Output the result
    print(max_length)
    print(" ".join(map(str, best_circle)))

if __name__ == "__main__":
    main()