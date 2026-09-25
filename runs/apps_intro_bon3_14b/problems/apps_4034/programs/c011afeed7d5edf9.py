import sys

def can_color_to_sorted(s):
    n = len(s)
    sorted_s = sorted(s)
    
    # Try to color the string such that we can sort it using swaps
    color = [0] * n
    
    for i in range(n):
        if s[i] != sorted_s[i]:
            # Find the next position where we can swap to get the correct character
            j = i + 1
            while j < n and (s[j] != sorted_s[i] or color[j] == color[i]):
                j += 1
            
            if j == n:
                return "NO", []
            
            # Swap the characters
            s[i], s[j] = s[j], s[i]
            color[i], color[j] = color[j], color[i]
    
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