import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:]))
    
    if k > len(set(a)):
        print("NO")
        return
    
    a.sort()
    colors = [0] * n
    color_index = 0
    
    for i in range(n):
        if colors[i] == 0:
            color_index += 1
            if color_index > k:
                print("NO")
                return
            colors[i] = color_index
            for j in range(i + 1, n):
                if a[j] != a[i]:
                    break
                colors[j] = color_index
    
    print("YES")
    print(" ".join(map(str, colors)))

if __name__ == "__main__":
    main()