import sys

def can_color_to_sort(s):
    n = len(s)
    sorted_s = sorted(s)
    
    # Create a coloring based on the sorted order
    coloring = ['0'] * n
    last_char = None
    
    for i in range(n):
        if s[i] != sorted_s[i]:
            if last_char == s[i]:
                coloring[i] = '1'
            else:
                coloring[i] = '0'
            last_char = s[i]
    
    return coloring

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    coloring = can_color_to_sort(s)
    
    if coloring is None:
        print("NO")
    else:
        print("YES")
        print(''.join(coloring))

if __name__ == "__main__":
    main()