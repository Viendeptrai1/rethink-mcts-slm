import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:]))
    
    if len(set(a)) < k:
        print("NO")
        return
    
    color_map = {}
    color_index = 1
    colors = []
    
    for num in a:
        if num not in color_map:
            if color_index > k:
                print("NO")
                return
            color_map[num] = color_index
            color_index += 1
        colors.append(color_map[num])
    
    print("YES")
    print(" ".join(map(str, colors)))

if __name__ == "__main__":
    main()