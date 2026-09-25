import sys

def can_color_to_sorted(s):
    n = len(s)
    # Check if the string is already sorted
    if s == ''.join(sorted(s)):
        return "YES", "0" * n
    
    # Try to color the string
    color = [0] * n
    for i in range(1, n):
        if s[i] < s[i - 1]:
            if color[i - 1] == 0:
                color[i - 1] = 1
            else:
                color[i] = 1
    
    # Check if the string can be sorted with the given coloring
    sorted_s = list(s)
    for i in range(n - 1):
        if color[i] != color[i + 1] and sorted_s[i] > sorted_s[i + 1]:
            sorted_s[i], sorted_s[i + 1] = sorted_s[i + 1], sorted_s[i]
    
    if ''.join(sorted_s) == ''.join(sorted(s)):
        return "YES", ''.join(map(str, color))
    else:
        return "NO", ""

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