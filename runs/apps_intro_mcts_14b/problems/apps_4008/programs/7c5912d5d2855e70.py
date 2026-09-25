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
    
    color_map = {}
    color_count = [0] * (k + 1)
    colors = []
    
    for num in a:
        if num in color_map:
            colors.append(color_map[num])
        else:
            for i in range(1, k + 1):
                if color_count[i] == 0:
                    color_map[num] = i
                    color_count[i] = 1
                    colors.append(i)
                    break
            else:
                print("NO")
                return
    
    print("YES")
    print(" ".join(map(str, colors)))

if __name__ == "__main__":
    main()