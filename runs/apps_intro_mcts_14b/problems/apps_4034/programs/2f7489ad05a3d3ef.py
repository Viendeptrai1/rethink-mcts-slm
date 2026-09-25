import sys

def can_be_sorted_by_swapping(s):
    n = len(s)
    sorted_s = sorted(s)
    
    # Create a mapping from character to its position in the sorted string
    pos_in_sorted = {char: [] for char in set(s)}
    for i, char in enumerate(sorted_s):
        pos_in_sorted[char].append(i)
    
    # Assign colors based on the positions in the sorted string
    colors = [''] * n
    current_color = 0
    
    for i, char in enumerate(s):
        # Find the next position of this character in the sorted string
        next_pos = pos_in_sorted[char].pop(0)
        
        # If the current position is greater than the next position, we need to swap
        if i > next_pos:
            return "NO"
        
        # Assign the current color to this character
        colors[i] = str(current_color)
        
        # Alternate the color for the next character
        current_color = 1 - current_color
    
    return "YES", ''.join(colors)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    result, coloring = can_be_sorted_by_swapping(s)
    print(result)
    if result == "YES":
        print(coloring)

if __name__ == "__main__":
    main()