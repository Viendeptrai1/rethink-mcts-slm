import sys

def can_color_to_sort(s):
    n = len(s)
    # Create a sorted version of the string
    sorted_s = sorted(s)
    
    # Try to find a valid coloring
    for color1 in ['0', '1']:
        color2 = '1' if color1 == '0' else '0'
        current_color = color1
        valid = True
        for i in range(n):
            if s[i] != sorted_s[i]:
                valid = False
                break
            if i > 0 and s[i] == s[i-1]:
                if current_color == color1:
                    current_color = color2
                else:
                    current_color = color1
            if s[i] == sorted_s[i] and current_color != color1:
                valid = False
                break
        if valid:
            return True, ''.join([color1 if s[i] == sorted_s[i] else color2 for i in range(n)])
    
    return False, ""

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    possible, coloring = can_color_to_sort(s)
    if possible:
        print("YES")
        print(coloring)
    else:
        print("NO")

if __name__ == "__main__":
    main()