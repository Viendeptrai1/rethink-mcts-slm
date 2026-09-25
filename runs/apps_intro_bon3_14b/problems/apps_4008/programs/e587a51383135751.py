import sys
from collections import defaultdict

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
    
    color_map = defaultdict(list)
    for i, x in enumerate(a):
        color_map[x].append(i)
    
    colors = [0] * n
    current_color = 1
    
    for indices in color_map.values():
        for index in indices:
            colors[index] = current_color
            current_color += 1
            if current_color > k:
                current_color = 1
    
    print("YES")
    print(" ".join(map(str, colors)))

if __name__ == "__main__":
    main()