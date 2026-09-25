import sys
from collections import Counter

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:]))
    
    unique_elements = len(set(a))
    
    if unique_elements < k:
        print("NO")
    else:
        print("YES")
        color_map = {}
        color_index = 1
        result = []
        
        for num in a:
            if num not in color_map:
                color_map[num] = color_index
                color_index += 1
                if color_index > k:
                    color_index = 1
            result.append(color_map[num])
        
        print(" ".join(map(str, result)))

if __name__ == "__main__":
    main()