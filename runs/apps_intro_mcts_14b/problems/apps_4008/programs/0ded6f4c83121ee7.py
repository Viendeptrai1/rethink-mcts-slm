import sys
from collections import Counter

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:]))
    
    unique_elements = set(a)
    
    if len(unique_elements) < k:
        print("NO")
    else:
        print("YES")
        color_map = {}
        colors = list(range(1, k + 1))
        color_index = 0
        
        for num in a:
            if num not in color_map:
                color_map[num] = colors[color_index]
                color_index += 1
                if color_index == k:
                    color_index = 0
        
        result = [str(color_map[num]) for num in a]
        print(" ".join(result))

if __name__ == "__main__":
    main()