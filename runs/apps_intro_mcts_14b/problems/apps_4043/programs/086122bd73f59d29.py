import sys

def construct_tree(n, d, k):
    if d >= n - 1:
        if k >= 2:
            print("YES")
            for i in range(1, n):
                print(i, i + 1)
            return
        else:
            print("NO")
            return
    
    if d < n - 1:
        if k >= 3:
            print("YES")
            # Create a path of length d+1
            for i in range(1, d + 2):
                print(i, i + 1)
            
            # Attach the remaining vertices to the path
            current = d + 2
            for i in range(d + 2, n + 1):
                print(1, i)
                current += 1
            
            return
        else:
            print("NO")
            return

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    d = int(data[1])
    k = int(data[2])
    
    construct_tree(n, d, k)

if __name__ == "__main__":
    main()