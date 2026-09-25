import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    M = int(data[2])
    A = list(map(int, data[3:]))
    
    current_sum = sum(A)
    total_required = M * N
    
    if current_sum + K < total_required:
        print(-1)
    else:
        min_score_needed = max(0, total_required - current_sum)
        print(min_score_needed)

if __name__ == "__main__":
    main()