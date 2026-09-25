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
    for i in range(n):
        if colors[i] == 0:
            colors[i] = color_index
            for j in range(i + 1, n):
                if a[j] == a[i]:
                    colors[j] = color_index
            color_index += 1
    
    # Check if all colors are used
    if max(colors) != k:
        print("NO")
        return
    
    # Print the result
    print("YES")
    print(" ".join(map(str, colors)))

if __name__ == "__main__":
    main()