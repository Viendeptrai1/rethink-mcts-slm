import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    Q = int(data[2])
    
    # Count how many times each player answered correctly
    answer_counts = [0] * (N + 1)
    idx = 3
    for _ in range(Q):
        player = int(data[idx])
        answer_counts[player] += 1
        idx += 1
    
    # Calculate final scores
    # Initial score: K
    # For each correct answer by someone else: -1
    # So final score = K - (total answers - own answers)
    #               = K - Q + own_answers
    
    for i in range(1, N + 1):
        own_answers = answer_counts[i]
        final_score = K - Q + own_answers
        if final_score > 0:
            print("Yes")
        else:
            print("No")

if __name__ == "__main__":
    solve()