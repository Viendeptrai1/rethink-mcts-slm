import sys

def can_be_sorted_by_swaps(s):
    n = len(s)
    sorted_s = sorted(s)
    
    # Create a list to store the color of each character
    colors = [0] * n
    
    # Try to color the string such that it can be sorted by swaps
    for i in range(n):
        if s[i] != sorted_s[i]:
            # Find the position of the correct character for s[i]
            j = i + 1
            while j < n and s[j] != sorted_s[i]:
                j += 1
            
            if j == n:
                return "NO", []
            
            # Swap s[i] with s[j] and color them differently
            s[i], s[j] = s[j], s[i]
            colors[i] = 1
            colors[j] = 0
    
    return "YES", colors

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    result, colors = can_be_sorted_by_swaps(list(s))
    
    print(result)
    if result == "YES":
        print("".join(map(str, colors)))

if __name__ == "__main__":
    main()