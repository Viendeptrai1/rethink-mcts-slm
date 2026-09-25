import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    d = int(data[1])
    k = int(data[2])
    
    if d < n - 1:
        print("NO")
        return
    
    if k == 1:
        if n > 2:
            print("NO")
        else:
            print("YES")
            print("1 2")
        return
    
    if k == 2:
        if d % 2 == 0:
            print("NO")
        else:
            print("YES")
            for i in range(1, n):
                print(i, i + 1)
        return
    
    if k >= 3:
        print("YES")
        # Create a path of length d
        for i in range(1, d):
            print(i, i + 1)
        
        # Attach remaining vertices to the path
        for i in range(d + 1, n):
            print(1, i)
        
        # Ensure no vertex has degree more than k
        if d + 1 < n:
            for i in range(d + 2, n):
                print(2, i)
        return

if __name__ == "__main__":
    main()