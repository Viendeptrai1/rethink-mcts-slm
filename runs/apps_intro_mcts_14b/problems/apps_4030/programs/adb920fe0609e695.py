import sys

def min_colors_to_sort(s):
    n = len(s)
    colors = [0] * n
    current_color = 1
    
    for i in range(n):
        if i == 0 or s[i] >= s[i - 1]:
            colors[i] = current_color
        else:
            colors[i] = current_color + 1
            current_color += 1
    
    return current_color, colors

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    res, c = min_colors_to_sort(s)
    
    print(res)
    print(' '.join(map(str, c)))

if __name__ == "__main__":
    main()