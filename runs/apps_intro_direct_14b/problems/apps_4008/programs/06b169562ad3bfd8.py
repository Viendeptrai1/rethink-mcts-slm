import sys
from collections import Counter

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:]))
    
    # Count the frequency of each element in the array
    freq = Counter(a)
    
    # Check if it's possible to color the array with k colors
    if len(freq) < k:
        print("NO")
        return
    
    # Create a list to store the colors
    colors = [0] * n
    
    # Assign colors to the elements
    color_index = 1
    color_count = {}
    
    for i in range(n):
        if a[i] not in color_count or color_count[a[i]] < k:
            if color_index > k:
                print("NO")
                return
            colors[i] = color_index
            color_count[a[i]] = color_count.get(a[i], 0) + 1
            if color_count[a[i]] == k:
                color_index += 1
        else:
            print("NO")
            return
    
    print("YES")
    print(" ".join(map(str, colors)))

if __name__ == "__main__":
    main()