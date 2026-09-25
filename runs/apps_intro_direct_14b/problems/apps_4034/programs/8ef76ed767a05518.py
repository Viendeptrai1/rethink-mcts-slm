import sys

def can_sort_by_coloring(s):
    n = len(s)
    # Create a sorted version of the string
    sorted_s = sorted(s)
    
    # Try to color the string such that we can sort it using swaps
    color = [0] * n
    used_colors = {0}
    
    for i in range(n):
        if s[i] != sorted_s[i]:
            # Find the next available color
            next_color = 1 - color[i]
            if next_color not in used_colors:
                used_colors.add(next_color)
                color[i] = next_color
            else:
                return "NO"
    
    return "YES", ''.join(map(str, color))

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    result, coloring = can_sort_by_coloring(s)
    print(result)
    if result == "YES":
        print(coloring)

if __name__ == "__main__":
    main()