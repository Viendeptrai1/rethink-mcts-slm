import sys

def solve():
    lines = sys.stdin.read().strip().split('\n')
    if not lines:
        return
    c = []
    for line in lines:
        row = list(map(int, line.split()))
        c.append(row)
    
    # Check the condition: c[i][j] - c[i][0] should be independent of i
    # That is, c[i][j] - c[i][0] == c[0][j] - c[0][0] for all i, j
    # Equivalently, c[i][j] + c[0][0] == c[i][0] + c[0][j]
    
    base = c[0][0]
    for i in range(3):
        for j in range(3):
            if c[i][j] + base != c[i][0] + c[0][j]:
                print("No")
                return
    print("Yes")

if __name__ == "__main__":
    solve()