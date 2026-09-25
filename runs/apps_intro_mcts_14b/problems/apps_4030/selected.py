import sys

def min_colors_to_sort(s):
    n = len(s)
    inversions = 0
    colors = [0] * n
    
    # Count inversions and assign colors
    current_color = 1
    for i in range(n):
        if i > 0 and s[i] < s[i - 1]:
            inversions += 1
            current_color += 1
        colors[i] = current_color
    
    return inversions + 1, colors

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    res, c = min_colors_to_sort(s)
    
    print(res)
    print(" ".join(map(str, c)))

if __name__ == "__main__":
    main()