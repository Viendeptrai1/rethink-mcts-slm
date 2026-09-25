import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    M = int(data[2])
    A = list(map(int, data[3:]))
    
    total_score_needed = M * N
    current_total_score = sum(A)
    score_needed_on_last_subject = total_score_needed - current_total_score
    
    if score_needed_on_last_subject < 0:
        score_needed_on_last_subject = 0
    
    if score_needed_on_last_subject > K:
        print(-1)
    else:
        print(score_needed_on_last_subject)

if __name__ == "__main__":
    main()