import sys

def solve(n, d, k):
    if d == 1:
        if n <= k + 1:
            print("YES")
            for i in range(2, n + 1):
                print(1, i)
        else:
            print("NO")
        return
    
    if d % 2 == 0:
        m = d // 2
    else:
        m = d // 2 + 1
    
    if n < 2 * m + 1:
        print("NO")
        return
    
    if k < 3:
        print("NO")
        return
    
    print("YES")
    
    # Create the main path of length d
    for i in range(2, m + 1):
        print(1, i)
    for i in range(m + 2, 2 * m + 2):
        print(i, 2 * m + 2 - i)
    
    # Attach the remaining vertices
    remaining_vertices = n - (2 * m + 1)
    for i in range(2 * m + 3, n + 1):
        print(3, i)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    d = int(data[1])
    k = int(data[2])
    
    solve(n, d, k)

if __name__ == "__main__":
    main()