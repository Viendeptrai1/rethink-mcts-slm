import sys

def can_color_to_sorted(s):
    n = len(s)
    # Check if the string is already sorted
    if s == ''.join(sorted(s)):
        return "YES", "0" * n
    
    # Try to find a valid coloring
    for color1 in range(26):
        for color2 in range(color1 + 1, 26):
            # Create a candidate coloring
            coloring = []
            used_color1 = False
            used_color2 = False
            
            for char in s:
                if ord(char) == color1 + ord('a'):
                    if not used_color1:
                        coloring.append('0')
                        used_color1 = True
                    else:
                        coloring.append('1')
                        used_color2 = True
                elif ord(char) == color2 + ord('a'):
                    if not used_color2:
                        coloring.append('1')
                        used_color2 = True
                    else:
                        coloring.append('0')
                        used_color1 = True
                else:
                    if used_color1 and used_color2:
                        break
                    if not used_color1:
                        coloring.append('0')
                        used_color1 = True
                    else:
                        coloring.append('1')
                        used_color2 = True
            
            if len(coloring) == n:
                # Check if the string can be sorted with this coloring
                sorted_s = ''.join(sorted(s))
                sorted_by_coloring = []
                i, j = 0, 0
                while i < n and j < n:
                    if coloring[i] == '0':
                        sorted_by_coloring.append(sorted_s[j])
                        j += 1
                    else:
                        sorted_by_coloring.append(sorted_s[j])
                        j += 1
                    i += 1
                
                if ''.join(sorted_by_coloring) == sorted_s:
                    return "YES", ''.join(coloring)
    
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