import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    M = int(data[1])
    
    A = data[2:2+N]
    B = data[2+N:]
    
    def contains_template(A, B, N, M):
        for i in range(N - M + 1):
            for j in range(N - M + 1):
                match = True
                for x in range(M):
                    for y in range(M):
                        if A[i + x][j + y] != B[x][y]:
                            match = False
                            break
                    if not match:
                        break
                if match:
                    return "Yes"
        return "No"
    
    print(contains_template(A, B, N, M))

if __name__ == "__main__":
    main()