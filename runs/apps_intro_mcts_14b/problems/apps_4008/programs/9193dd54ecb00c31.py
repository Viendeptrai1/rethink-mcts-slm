import sys

def main():
    import sys
    import collections
    
    def read_ints():
        return list(map(int, sys.stdin.readline().split()))
    
    n, k = read_ints()
    a = read_ints()
    
    # Count the frequency of each element
    freq = collections.Counter(a)
    
    # Check if it's possible to color the array
    if len(freq) < k:
        print("NO")
        return
    
    # Sort elements by their frequency in descending order
    sorted_elements = sorted(freq.keys(), key=lambda x: -freq[x])
    
    # Assign colors
    color = {}
    current_color = 1
    for element in sorted_elements:
        if current_color > k:
            break
        color[element] = current_color
        current_color += 1
    
    # Check if we have enough colors
    if len(color) < k:
        print("NO")
        return
    
    # Assign colors to the array
    result = []
    for element in a:
        result.append(color[element])
    
    print("YES")
    print(" ".join(map(str, result)))

if __name__ == "__main__":
    main()