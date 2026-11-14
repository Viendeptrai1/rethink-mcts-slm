import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    idx = 0
    
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    
    a = []
    for _ in range(n):
        row = []
        for _ in range(m):
            row.append(int(data[idx])); idx += 1
        a.append(row)
        
    b = []
    for _ in range(n):
        row = []
        for _ in range(m):
            row.append(int(data[idx])); idx += 1
        b.append(row)
        
    # Greedy strategy: For every cell (i, j), ensure a[i][j] is the minimum and b[i][j] is the maximum of the pair.
    # This is because having the smaller number in the first matrix and larger in the second gives the best chance
    # for both matrices to be strictly increasing (smaller values help satisfy < constraints from left/top).
    for i in range(n):
        for j in range(m):
            if a[i][j] > b[i][j]:
                a[i][j], b[i][j] = b[i][j], a[i][j]
                
    # Check if matrix a is strictly increasing
    for i in range(n):
        for j in range(m - 1):
            if a[i][j] >= a[i][j+1]:
                print("Impossible")
                return
    for j in range(m):
        for i in range(n - 1):
            if a[i][j] >= a[i+1][j]:
                print("Impossible")
                return
                
    # Check if matrix b is strictly increasing
    for i in range(n):
        for j in range(m - 1):
            if b[i][j] >= b[i][j+1]:
                print("Impossible")
                return
    for j in range(m):
        for i in range(n - 1):
            if b[i][j] >= b[i+1][j]:
                print("Impossible")
                return
                
    print("Possible")

if __name__ == "__main__":
    solve()