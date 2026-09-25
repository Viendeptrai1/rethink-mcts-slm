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
    
    # Create a dictionary to store the effect of each segment
    effect = defaultdict(int)
    for i, (l, r) in enumerate(segments):
        effect[l] += 1
        if r + 1 < n:
            effect[r + 1] -= 1
    
    # Calculate the prefix sum to get the actual effect of each position
    current_effect = 0
    for i in range(n):
        current_effect += effect[i]
        a[i] -= current_effect
    
    # Find the maximum and minimum values in the modified array
    max_val = max(a)
    min_val = min(a)
    
    # The result is the difference between the maximum and minimum values
    result = max_val - min_val
    
    # To find the segments that were used, we need to track the effect again
    used_segments = []
    current_effect = 0
    for i, (l, r) in enumerate(segments):
        current_effect += effect[l]
        if current_effect > 0:
            used_segments.append(i + 1)
    
    # Print the result
    print(result)
    print(len(used_segments))
    print(*used_segments)

if __name__ == "__main__":
    main()