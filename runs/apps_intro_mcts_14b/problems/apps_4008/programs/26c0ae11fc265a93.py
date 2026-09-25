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
    
    # Check if the number of unique elements is at least k
    if len(freq) < k:
        print("NO")
        return
    
    # Sort the elements by their value
    sorted_a = sorted(a)
    
    # Initialize the result array with zeros
    result = [0] * n
    
    # Assign colors
    color = 1
    color_count = {}
    
    for i in range(n):
        if sorted_a[i] not in color_count or color_count[sorted_a[i]] == 0:
            result[i] = color
            color_count[sorted_a[i]] = 1
            color += 1
            if color > k:
                color = 1
        else:
            result[i] = color
            color_count[sorted_a[i]] += 1
    
    # Ensure each color is used at least once
    if len(set(result)) != k:
        print("NO")
        return
    
    print("YES")
    print(" ".join(map(str, result)))

if __name__ == "__main__":
    main()