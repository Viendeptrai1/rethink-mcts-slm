import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    M = int(data[2])
    A = list(map(int, data[3:]))
    
    total_required = M * N
    current_total = sum(A)
    needed_score = total_required - current_total
    
    if needed_score < 0:
        needed_score = 0
    
    if needed_score > K:
        print(-1)
    else:
        print(needed_score)

if __name__ == "__main__":
    main()