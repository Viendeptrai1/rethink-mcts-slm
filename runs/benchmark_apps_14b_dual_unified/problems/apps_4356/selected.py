import sys

def is_template_in_image(N, M, A, B):
    for i in range(N - M + 1):
        for j in range(N - M + 1):
            match = True
            for x in range(M):
                for y in range(M):
                    if B[x][y] == '#' and A[i + x][j + y] != '#':
                        match = False
                        break
                if not match:
                    break
            if match:
                return "Yes"
    return "No"

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    M = int(data[1])
    
    A = data[2:N+2]
    B = data[N+2:]
    
    result = is_template_in_image(N, M, A, B)
    print(result)

if __name__ == "__main__":
    main()