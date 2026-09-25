import sys
from collections import defaultdict

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    m = int(data[index + 1])
    index += 2
    
    a = list(map(int, data[index:index + n]))
    index += n
    
    segments = []
    for _ in range(m):
        l = int(data[index]) - 1
        r = int(data[index + 1]) - 1
        segments.append((l, r))
        index += 2
    
    # Initialize the difference array
    diff = [0] * (n + 1)
    
    # Apply the segments to the difference array
    for l, r in segments:
        diff[l] -= 1
        diff[r + 1] += 1
    
    # Compute the prefix sum to get the final array b
    b = [0] * n
    current = 0
    for i in range(n):
        current += diff[i]
        b[i] = a[i] + current
    
    # Find the maximum and minimum values in b
    max_b = max(b)
    min_b = min(b)
    
    # Calculate the initial difference
    result_diff = max_b - min_b
    
    # Try to improve the result by removing segments
    best_diff = result_diff
    best_segments = []
    
    for i in range(m):
        l, r = segments[i]
        # Temporarily remove the segment
        diff[l] += 1
        diff[r + 1] -= 1
        
        # Recompute the prefix sum
        current = 0
        for j in range(n):
            current += diff[j]
            b[j] = a[j] + current
        
        # Find the new maximum and minimum values
        max_b = max(b)
        min_b = min(b)
        
        # Calculate the new difference
        new_diff = max_b - min_b
        
        # If the new difference is better, update the result
        if new_diff > best_diff:
            best_diff = new_diff
            best_segments = [i + 1]
        elif new_diff == best_diff:
            best_segments.append(i + 1)
        
        # Reapply the segment
        diff[l] -= 1
        diff[r + 1] += 1
    
    # Print the result
    print(best_diff)
    print(len(best_segments))
    print(' '.join(map(str, best_segments)))

if __name__ == "__main__":
    main()