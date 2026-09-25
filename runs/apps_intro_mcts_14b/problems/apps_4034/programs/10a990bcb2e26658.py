import sys

def can_color_to_sorted(s):
    n = len(s)
    if s == ''.join(sorted(s)):
        return "YES", "0" * n
    
    # Try to find a valid coloring
    for color1 in range(26):
        for color2 in range(color1 + 1, 26):
            colored = []
            for char in s:
                if ord(char) == color1 + ord('a'):
                    colored.append('0')
                elif ord(char) == color2 + ord('a'):
                    colored.append('1')
                else:
                    break
            else:
                # Check if we can sort with this coloring
                sorted_colored = sorted(colored)
                if sorted_colored == colored:
                    return "YES", ''.join(colored)
    
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