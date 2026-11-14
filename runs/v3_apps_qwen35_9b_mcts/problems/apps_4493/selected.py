import sys

def solve():
    lines = sys.stdin.read().split()
    if len(lines) < 9:
        return
    
    c = []
    for i in range(3):
        row = [int(lines[i*3 + j]) for j in range(3)]
        c.append(row)
    
    # Check if c[i][j] = a[i] + b[j]
    # This implies c[i][j] - c[i][k] = b[j] - b[k] (independent of i)
    # So the difference between any two columns must be the same for all rows.
    # Similarly, difference between any two rows must be the same for all columns.
    
    # Check column differences
    for j in range(2):
        for i in range(2):
            if c[i][j] - c[i][j+1] != c[i+1][j] - c[i+1][j+1]:
                print("No")
                return
    
    # Check row differences
    for i in range(2):
        for j in range(2):
            if c[i][j] - c[i+1][j] != c[i][j+1] - c[i+1][j+1]:
                print("No")
                return
    
    print("Yes")

if __name__ == "__main__":
    solve()