import sys

def can_color_to_sort(s):
    n = len(s)
    sorted_s = sorted(s)
    
    # Create a mapping from character to its position in the sorted string
    pos_map = {char: [] for char in set(s)}
    for i, char in enumerate(sorted_s):
        pos_map[char].append(i)
    
    # Initialize the coloring
    coloring = [-1] * n
    
    # Try to color the string
    for i, char in enumerate(s):
        # Find the smallest position in the sorted string that hasn't been used yet
        for pos in pos_map[char]:
            if coloring[pos] == -1:
                coloring[pos] = i % 2
                break
    
    # Check if the coloring is valid
    for i in range(n - 1):
        if s[i] > s[i + 1] and coloring[i] == coloring[i + 1]:
            return "NO"
    
    # Convert coloring to string
    coloring_str = ''.join(map(str, coloring))
    return "YES", coloring_str

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    result, coloring = can_color_to_sort(s)
    print(result)
    if result == "YES":
        print(coloring)

if __name__ == "__main__":
    main()