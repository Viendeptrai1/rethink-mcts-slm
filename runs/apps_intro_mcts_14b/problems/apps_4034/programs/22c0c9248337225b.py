import sys

def can_be_sorted_by_swaps(s):
    n = len(s)
    # Create a list of tuples (character, index)
    indexed_s = list(enumerate(s))
    # Sort the list by character
    indexed_s.sort(key=lambda x: x[1])
    
    # Check if we can color the string such that it can be sorted by swaps
    color = [0] * n
    last_color = 0
    
    for i in range(n):
        if i > 0 and indexed_s[i][1] < indexed_s[i - 1][1]:
            # If the current character is less than the previous one, we need to color it differently
            last_color = 1 - last_color
        color[indexed_s[i][0]] = last_color
    
    # Verify if the coloring allows sorting
    for i in range(1, n):
        if s[i] < s[i - 1] and color[i] == color[i - 1]:
            return "NO"
    
    return "YES", ''.join(map(str, color))

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    result, coloring = can_be_sorted_by_swaps(s)
    print(result)
    if result == "YES":
        print(coloring)

if __name__ == "__main__":
    main()