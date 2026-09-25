import sys

def min_colors_to_sort(s):
    n = len(s)
    colors = [1] * n
    current_color = 1
    
    for i in range(1, n):
        if s[i] < s[i - 1]:
            current_color += 1
        colors[i] = current_color
    
    return current_color, colors

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    res, c = min_colors_to_sort(s)
    
    sys.stdout.write(f"{res}\n")
    sys.stdout.write(" ".join(map(str, c)))

if __name__ == "__main__":
    main()