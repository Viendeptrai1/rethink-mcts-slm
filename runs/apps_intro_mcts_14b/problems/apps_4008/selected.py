import sys
from collections import Counter

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:]))
    
    # Count the frequency of each element
    freq = Counter(a)
    
    # Check if we have at least k unique elements
    if len(freq) < k:
        print("NO")
        return
    
    # Create a list of colors
    colors = [0] * n
    color_index = 1
    
    # Assign colors to elements
    for i in range(n):
        if colors[i] == 0:
            colors[i] = color_index
            color_index += 1
            if color_index > k:
                color_index = 1
    
    # Ensure each color is used at least once
    color_count = Counter(colors)
    if min(color_count.values()) < 1:
        print("NO")
        return
    
    # Ensure all elements of the same color are distinct
    for i in range(n):
        for j in range(i + 1, n):
            if a[i] == a[j] and colors[i] == colors[j]:
                print("NO")
                return
    
    print("YES")
    print(" ".join(map(str, colors)))

if __name__ == "__main__":
    main()