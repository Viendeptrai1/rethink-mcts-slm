import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        A = [next(iterator) for _ in range(N)]
        B = [next(iterator) for _ in range(M)]
    except StopIteration:
        return

    for r in range(N - M + 1):
        for c in range(N - M + 1):
            match = True
            for i in range(M):
                for j in range(M):
                    if A[r + i][c + j] != B[i][j]:
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