import sys

def can_color_to_sorted(s):
    n = len(s)
    sorted_s = sorted(s)
    
    # Create a mapping from character to its position in the sorted string
    pos_map = {char: [] for char in set(sorted_s)}
    for i, char in enumerate(sorted_s):
        pos_map[char].append(i)
    
    # Check if we can color the string
    color = [None] * n
    current_color = 0
    
    for i, char in enumerate(s):
        if color[i] is None:
            # Find the next available position for this character in the sorted string
            next_pos = pos_map[char][0]
            color[i] = current_color
            
            # Mark this position as used
            pos_map[char].pop(0)
            
            # Alternate the color for the next character
            current_color = 1 - current_color
    
    # Verify the coloring
    for i in range(n - 1):
        if s[i] > s[i + 1] and color[i] == color[i + 1]:
            return "NO", []
    
    return "YES", ''.join(map(str, color))

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    result, coloring = can_color_to_sorted(s)
    print(result)
    if result == "YES":
        print(coloring)

if __name__ == "__main__":
    main()