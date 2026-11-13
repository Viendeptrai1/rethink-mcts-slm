import sys
from collections import defaultdict

def main():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    Q = int(data[2])
    
    scores = [K] * N
    score_changes = defaultdict(int)
    
    index = 3
    for _ in range(Q):
        player = int(data[index]) - 1
        index += 1
        scores[player] -= 1
        score_changes[player] += 1
    
    for i in range(N):
        scores[i] += score_changes[i]
    
    for score in scores:
        if score > 0:
            print("Yes")
        else:
            print("No")

if __name__ == "__main__":
    main()