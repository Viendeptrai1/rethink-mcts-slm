import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    iterator = iter(data)
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        
        A = []
        for _ in range(N):
            A.append(next(iterator))
            
        B = []
        for _ in range(M):
            B.append(next(iterator))
    except StopIteration:
        return

    # Check every possible top-left position (i, j) in A where B can fit
    # i ranges from 0 to N-M
    # j ranges from 0 to N-M
    for i in range(N - M + 1):
        for j in range(N - M + 1):
            match = True
            # Check if B matches the subimage of A starting at (i, j)
            for r in range(M):
                for c in range(M):
                    if A[i + r][j + c] != B[r][c]:
                        match = False
                        break
                if not match:
                    break
            if match:
                print("Yes")
                return

    print("No")

if __name__ == "__main__":
    solve()