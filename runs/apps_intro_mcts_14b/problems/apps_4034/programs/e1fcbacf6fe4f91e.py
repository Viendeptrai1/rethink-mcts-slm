import sys

def can_color_and_sort(s):
    n = len(s)
    sorted_s = sorted(s)
    
    # Create a mapping from character to its position in the sorted string
    pos_map = {char: [] for char in set(s)}
    for i, char in enumerate(sorted_s):
        pos_map[char].append(i)
    
    # Try to assign colors
    color = [None] * n
    current_color = 0
    
    for i, char in enumerate(s):
        if color[i] is None:
            # Find the next available position for this character in the sorted string
            for pos in pos_map[char]:
                if color[pos] is None:
                    color[pos] = current_color
                    break
            else:
                return "NO"
        
        # Alternate the color for the next character
        current_color = 1 - current_color
    
    # Check if the coloring allows sorting
    for i in range(n - 1):
        if s[i] > s[i + 1] and color[i] == color[i + 1]:
            return "NO"
    
    return "YES", ''.join(map(str, color))

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    result = can_color_and_sort(s)
    if result == "NO":
        print("NO")
    else:
        print("YES")
        print(result[1])

if __name__ == "__main__":
    main()