import sys

def solve():
    input = sys.stdin.read().split()
    if not input:
        return
    
    iterator = iter(input)
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

    # Check every possible top-left position (i, j) where B can fit in A
    # i ranges from 0 to N-M
    # j ranges from 0 to N-M
    for i in range(N - M + 1):
        for j in range(N - M + 1):
            match = True
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