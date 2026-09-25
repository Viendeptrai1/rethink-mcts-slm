import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    colors = [1] * n
    current_color = 1
    
    for i in range(1, n):
        if s[i] < s[i - 1]:
            current_color += 1
        colors[i] = current_color
    
    print(current_color)
    print(' '.join(map(str, colors)))

if __name__ == "__main__":
    main()