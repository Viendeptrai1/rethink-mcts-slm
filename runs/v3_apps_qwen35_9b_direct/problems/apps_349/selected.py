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
        
    # For each position (i, j), we have two choices:
    # 1. Keep a[i][j] in matrix A and b[i][j] in matrix B.
    # 2. Swap them: b[i][j] in matrix A and a[i][j] in matrix B.
    #
    # To maximize the chance of both matrices being strictly increasing,
    # for each position, we should assign the smaller value to matrix A and the larger value to matrix B.
    # Why? Because if we have a choice between (x, y) and (y, x) where x < y,
    # putting x in A and y in B gives us the "easiest" condition for A (smaller numbers) 
    # and the "easiest" condition for B (larger numbers) relative to neighbors.
    # Specifically, if we can form increasing sequences with the sorted assignment, 
    # we can definitely do it. If we can't, no other assignment will work because 
    # any other assignment would involve swapping some pairs, which would put a larger number 
    # in A (making it harder to be increasing) and a smaller number in B (making it harder).
    
    # Let's construct the two candidate matrices based on this logic.
    # Matrix A_final[i][j] = min(a[i][j], b[i][j])
    # Matrix B_final[i][j] = max(a[i][j], b[i][j])
    
    a_final = [[0]*m for _ in range(n)]
    b_final = [[0]*m for _ in range(n)]
    
    for i in range(n):
        for j in range(m):
            val1 = a[i][j]
            val2 = b[i][j]
            if val1 < val2:
                a_final[i][j] = val1
                b_final[i][j] = val2
            else:
                a_final[i][j] = val2
                b_final[i][j] = val1
                
    # Now check if a_final is strictly increasing
    def is_increasing(mat):
        # Check rows
        for i in range(n):
            for j in range(m-1):
                if mat[i][j] >= mat[i][j+1]:
                    return False
        # Check columns
        for j in range(m):
            for i in range(n-1):
                if mat[i][j] >= mat[i+1][j]:
                    return False
        return True

    if is_increasing(a_final) and is_increasing(b_final):
        print("Possible")
    else:
        print("Impossible")

if __name__ == "__main__":
    solve()